from dataclasses import dataclass, field

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


class Platform:

    def __init__(self):
        # unique ID
        self.platform_id = uuid.uuid4()

        # current status info
        self.platform_status = PlatformStatus()

        # sound power level, in decibels, at all stop
        self.baseline_sound_level = 50

    # define callback function for when message is received
    @staticmethod
    def on_message_callback(client: paho.mqtt.client.Client, userdata, msg: paho.mqtt.client.MQTTMessage):

        # message received
        print(f'[host:port:topic] = [{client.host}:{client.port}:{msg.topic}]')

        # message with PlatformStatus binary data
        if msg.topic == 'platform_status':
            # payload is a pickled PlatformStatus object (binary data)
            # noinspection PyTypeChecker
            platform_status: PlatformStatus = pickle.loads(msg.payload)
            for entry in platform_status.__dict__:
                print(f'    {entry}: {platform_status.__dict__[entry]}')

        # message with text data.  Note it is actually still binary, so we use .decode() to get the string version
        else:
            print(f'    {msg.payload}')
            print(f'    {msg.payload.decode('utf-8')}')

    def connect(self):
        """
        Connect to the MQTT data broker
        """
        # get data from ini file
        config.load()       # todo - we really only need to load the data once
        mqtt_host: str = config.config_data.get('MQTT-Broker', 'host')
        mqtt_port: int = config.config_data.getint('MQTT-Broker', 'port')

        my_client: paho.mqtt.client.Client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)

        # set the callback function to be called whenever a message is received
        my_client.on_message = Platform.on_message_callback

        # connect to MQTT broker
        if my_client.connect(host = mqtt_host, port = mqtt_port, keepalive = 60) != 0:
            print('Could not connect to MQTT broker')
            sys.exit(-1)

        # subscribe
        # my_client.subscribe(topic='platform_status')
        # my_client.subscribe(topic='general')
        my_client.subscribe(topic='+')

        # loop and listen for incoming messages
        try:
            print('Press CTRL-C to exit')
            my_client.loop_forever()
        except OSError:
            print('Connection to MQTT broker has failed')

        my_client.disconnect()


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
    platform.connect()


if __name__ == '__main__':
    main()
