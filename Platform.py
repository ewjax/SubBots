
import paho.mqtt.client
import sys
import uuid
import pickle

import Point


# define callback function for when message is received
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

    # message with text data.  Note it is still binary, so we use .decode() to get the string version
    else:
        print(f'    {msg.payload}')
        print(f'    {msg.payload.decode('utf-8')}')


#
# data class for all data for this platform, maintained by the simulation umpire
#
class PlatformStatus:

    def __init__(self):
        # cartesian (x,y) location
        self.location: Point = Point.Point(3,4)

        # in degrees and degrees/time
        self.course: float = 0.0
        self.course_ordered: float = 0.0
        self.turn_rate: float = 10.0

        # in feet (0 = surfaced) and feet/time
        self.depth: int = 0
        self.depth_ordered: int = 0
        self.depth_change_rate: int = 10

        # in knots and knots/time
        self.speed: float = 0
        self.speed_ordered: float = 0
        self.acceleration: float = 5

        # timestamp for this data point
        self.timestamp: str = ''

        # damage, 0 = sunk
        self.hull = 100


class Platform:

    def __init__(self):
        # unique ID
        self.platform_id = uuid.uuid4()

        # current status info
        self.platform_status = PlatformStatus()

        # sound power level, in decibels, at all stop
        self.baseline_sound_level = 50






def main():
    platform = Platform()
    platform_status = platform.platform_status

    print('---------------------------------------------------------------------')
    print('Platform:')
    for entry in platform.__dict__:
        print(f'{entry}: {platform.__dict__[entry]}')
    print('---------------------------------------------------------------------')
    print('PlatformStatus:')
    for entry in platform_status.__dict__:
        print(f'{entry}: {platform_status.__dict__[entry]}')
    print('---------------------------------------------------------------------')
    print('Binary serialization with pickle:')

    print(f'original = {platform_status}')
    pd = pickle.dumps(platform_status)
    print(f'pickled = {pd}')
    pu = pickle.loads(pd)
    print(f'unpickled = {pu}')

    print('---------------------------------------------------------------------')
    print('Listen for messages from MQTT broker:')

    my_client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)

    # set the callback function to be called whenever a message is received
    my_client.on_message = on_message_callback

    # connect to MQTT broker
    if my_client.connect(host = 'fourbee', port = 1883, keepalive = 60) != 0:
        print('Could not connect to MQTT broker')
        sys.exit(-1)

    # subscribe
    # my_client.subscribe(topic='test/hello_world')
    my_client.subscribe(topic = 'platform_status')
    my_client.subscribe(topic = 'general')

    # loop and listen for incoming messages
    try:
        print('Press CTRL-C to exit')
        my_client.loop_forever()
    except OSError:
        print('Connection to MQTT broker has failed')

    my_client.disconnect()


if __name__ == '__main__':
    main()
