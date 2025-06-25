from dataclasses import dataclass, field

from paho.mqtt.client import CallbackOnMessage
from paho.mqtt.enums import CallbackAPIVersion

import paho.mqtt.client
import sys
import uuid
import pickle
import datetime

import config
import Point


#
# data class for all data for this platform, maintained by the simulation umpire
#
# note use of @dataclass decorator to auto-create __init__, __repr__, and __eq__
@dataclass
class PlatformStatus:
    # cartesian (x,y) location
    location: Point.Point = field(default_factory=Point.Point)

    # in degrees and degrees/time
    course: float = 0.0
    course_ordered: float = 0.0
    turn_rate: float = 10.0

    # in feet (0 = surfaced) and feet/time
    depth: int = 0
    depth_ordered: int = 0
    depth_change_rate: int = 10

    # in knots and knots/time
    speed: float = 0
    speed_ordered: float = 0
    acceleration: float = 5

    # timestamp for this data point
    timestamp: datetime.datetime = datetime.datetime.now()

    # damage, 0 = sunk
    hull = 100


#
# intended as a base class for every craft present in the simulation
#
# derive from mqtt Client class
#
class Platform(paho.mqtt.client.Client):

    # ctor
    def __init__(self):
        """
        ctor
        """
        # call parent ctor
        super().__init__(CallbackAPIVersion.VERSION2)

        # unique ID
        self.platform_id = uuid.uuid4()

        # current status info
        self.platform_status = PlatformStatus()

        # sound power level, in decibels, at all stop
        self.baseline_sound_level = 50

        # control variable for mqtt loop
        self.processing = False

    #
    # virtual function to capture specific actions for any Platform child class
    #
    def command_and_control(self) -> None:
        """
        virtual function to capture specific actions for any Platform child class
        """
        # todo turn the exception back on after development and testing
        # raise NotImplementedError()
        pass

    #
    # function for user to call to connect, register, and begin listening and reacting to messages
    #
    def run(self) -> None:
        """
        function for user to call to connect, register, and begin listening and reacting to messages
        """
        # get config data from ini file
        config.load()
        mqtt_host: str = config.config_data.get('MQTT-Broker', 'host')
        mqtt_port: int = config.config_data.getint('MQTT-Broker', 'port')

        # connect to MQTT broker
        if self.connect(host = mqtt_host, port = mqtt_port, keepalive = 60) != 0:
            print('Could not connect to MQTT broker')
            sys.exit(-1)
        print(f'Connected to mqtt broker [host:port] = [{mqtt_host}:{mqtt_port}]')

        # subscribe to needed topics
        self.do_subscriptions()

        # set the processing boolean flag to True.  This will get set back to False when a 'disco' topic is received
        self.processing = True

        # begin processing loop
        while self.processing:

            # ensure mqtt pub and sub buffers are processed, with a 100 ms time delay
            self.loop(0.1)

            # do platform things here
            self.command_and_control()

            # todo what is needed to handle reconnections?

        # do loop cleanup
        self.loop_stop()
        self.disconnect()
        print(f'Disconnected from mqtt broker [host:port] = [{mqtt_host}:{mqtt_port}]')

    # manage all the mqtt topic subscriptions here
    def do_subscriptions(self) -> None:
        """
        Set up all the topic subscriptions for the mqtt client
        """
        self.subscribe(topic = 'platform_status')
        self.subscribe(topic = 'general')
        self.subscribe(topic = 'disco')


    # override the on_message callback
    # this function will get called for each message received
    def on_message(self, client: paho.mqtt.client.Client, userdata: any, msg: paho.mqtt.client.MQTTMessage) -> CallbackOnMessage | None:
        """
        Callback function that will be called any time a topic subscription is received
        :param client:
        :type client: paho.mqtt.client.Client
        :param userdata:
        :param msg:
        :type msg: paho.mqtt.client.MQTTMessage
        """

        # message received
        print(f'[host:port:topic] = [{self.host}:{self.port}:{msg.topic}]')

        # message with PlatformStatus binary data
        if msg.topic == 'platform_status':
            # payload is a pickled PlatformStatus object (binary data)
            # noinspection PyTypeChecker
            platform_status: PlatformStatus = pickle.loads(msg.payload)
            for entry in platform_status.__dict__:
                print(f'    {entry}: {platform_status.__dict__[entry]}')

        elif msg.topic == 'disco':
            print('    Disco message received')
            # this will cause the main Platform processing loop to break out
            self.processing = False

        # message with text data.  Note it is actually still binary, so we use .decode() to get the string version
        else:
            print(f'    {msg.payload}')
            print(f'    {msg.payload.decode('utf-8')}')





def main():
    my_bot = Platform()
    platform_status = my_bot.platform_status

    # print('---------------------------------------------------------------------')
    # print('Platform:')
    # for entry in generic_bot.__dict__:
    #     print(f'    {entry}: {generic_bot.__dict__[entry]}')
    # print('---------------------------------------------------------------------')
    print('PlatformStatus:')
    for entry in platform_status.__dict__:
        print(f'    {entry}: {platform_status.__dict__[entry]}')
    print('---------------------------------------------------------------------')
    print('Binary serialization with pickle:')

    print(f'original = {platform_status}')
    pd = pickle.dumps(platform_status)
    print(f'pickled = {pd}')
    pu = pickle.loads(pd)
    print(f'unpickled = {pu}')

    print('---------------------------------------------------------------------')
    print('Listen for messages from MQTT broker:')

    # initiate connection and begin listening
    my_bot.run()


if __name__ == '__main__':
    main()
