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
# note use of @dataclass annotation to auto-create __init__, __repr__, and __eq__
@dataclass
class PlatformStatus:
    # cartesian (x,y) location
    # location: Point.Point = Point.Point(3, 4)
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
# derive from mqtt Client class
#
class Platform(paho.mqtt.client.Client):

    # ctor
    def __init__(self, callback_api_version: CallbackAPIVersion = CallbackAPIVersion.VERSION2):

        # call parent ctor
        super().__init__(callback_api_version)

        # unique ID
        self.platform_id = uuid.uuid4()

        # current status info
        self.platform_status = PlatformStatus()

        # sound power level, in decibels, at all stop
        self.baseline_sound_level = 50

        self.processing = False

    def run(self):

        # get config data from ini file
        config.load()
        mqtt_host: str = config.config_data.get('MQTT-Broker', 'host')
        mqtt_port: int = config.config_data.getint('MQTT-Broker', 'port')

        # connect to MQTT broker
        if self.connect(host = mqtt_host, port = mqtt_port, keepalive = 60) != 0:
            print('Could not connect to MQTT broker')
            sys.exit(-1)

        # subscribe to needed topics
        self.do_subscriptions()

        # begin processing loop
        self.processing = True
        while self.processing:

            # do platform things here

            # ensure mqtt pub and sub queue's are processed, with a 100 ms delay
            self.loop(0.1)

            # do more platform things here

            # what is needed to handle reconnections?

        # do loop cleanup
        self.loop_stop()
        self.disconnect()
        print(f'Disconnected')


    # # connect to the mqtt broker
    # # this function becomes a blocking loop, listening for subs
    # def do_connect(self):
    #     """
    #     Connect to the MQTT data broker
    #     """
    #
    #     # subscribe
    #
    #     # loop and listen for incoming messages
    #     try:
    #         print('Press CTRL-C to exit')
    #         self.loop_forever()
    #     except OSError:
    #         print('Connection to MQTT broker has failed')
    #
    #     self.disconnect()

    # manage all the mqtt topic subscriptions here
    def do_subscriptions(self) -> None:
        """
        Set up all the topic subscriptions for the mqtt client
        """
        # my_client.subscribe(topic='platform_status')
        # my_client.subscribe(topic='general')
        self.subscribe(topic='+')

    # override the on_message callback
    def on_message(self, client, userdata, msg) -> CallbackOnMessage | None:

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
            self.processing = False

        # message with text data.  Note it is actually still binary, so we use .decode() to get the string version
        else:
            print(f'    {msg.payload}')
            print(f'    {msg.payload.decode('utf-8')}')




    # # define callback function for when message is received
    # @staticmethod
    # def on_message_callback(client: paho.mqtt.client.Client, userdata: any, msg: paho.mqtt.client.MQTTMessage) -> None:
    #     """
    #     Callback function that will be called any time a topic subscription is received
    #     :param client:
    #     :type client: paho.mqtt.client.Client
    #     :param userdata:
    #     :param msg:
    #     :type msg: paho.mqtt.client.MQTTMessage
    #     """
    #     # message received
    #     print(f'[host:port:topic] = [{client.host}:{client.port}:{msg.topic}]')
    #
    #     # message with PlatformStatus binary data
    #     if msg.topic == 'platform_status':
    #         # payload is a pickled PlatformStatus object (binary data)
    #         # noinspection PyTypeChecker
    #         platform_status: PlatformStatus = pickle.loads(msg.payload)
    #         for entry in platform_status.__dict__:
    #             print(f'    {entry}: {platform_status.__dict__[entry]}')
    #
    #     # message with text data.  Note it is actually still binary, so we use .decode() to get the string version
    #     else:
    #         print(f'    {msg.payload}')
    #         print(f'    {msg.payload.decode('utf-8')}')
    #

def main():
    platform = Platform()
    platform_status = platform.platform_status

    print('---------------------------------------------------------------------')
    print('Platform:')
    for entry in platform.__dict__:
        print(f'    {entry}: {platform.__dict__[entry]}')
    print('---------------------------------------------------------------------')
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
    platform.run()


if __name__ == '__main__':
    main()
