import paho.mqtt.client

from paho.mqtt.client import CallbackOnMessage
from paho.mqtt.enums import CallbackAPIVersion

import sys
import pickle

import config
import Platform


#
# intended as the class that governs Platform movements and interactions
#
# derive from mqtt Client class
#
class Umpire(paho.mqtt.client.Client):

    # ctor
    def __init__(self):
        """
        ctor
        """
        # call parent ctor
        super().__init__(CallbackAPIVersion.VERSION2)

        # control variable for mqtt loop
        self.processing = False


    # function that gets called while the mqtt comms loop is looping
    def process_time_tick(self) -> None:

        # binary message
        platform = Platform.Platform()
        # just to confirm the info gets pickled/unpickled correctly
        platform.platform_status.location.x = 7
        platform.platform_status.location.y = -9
        platform.platform_status.depth = 9999
        self.publish(topic = 'platform_status', payload = pickle.dumps(platform.platform_status), qos=0)

        # text message
        self.publish(topic = 'general', payload = 'Generic text message', qos = 0)

        # tell subscribers to disconnect
        self.publish(topic = 'disco', payload = '', qos = 0)

        # disconnect
        self.processing = False

    #
    # function for to call to connect, and begin listening and reacting to messages
    #
    def run(self) -> None:
        """
        function for to call to connect, and begin listening and reacting to messages
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
            self.process_time_tick()

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
        # self.subscribe(topic = 'platform_status')
        pass

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

        # # message with PlatformStatus binary data
        # if msg.topic == 'platform_status':
        #     # payload is a pickled PlatformStatus object (binary data)
        #     # noinspection PyTypeChecker
        #     platform_status: PlatformStatus = pickle.loads(msg.payload)
        #     for entry in platform_status.__dict__:
        #         print(f'    {entry}: {platform_status.__dict__[entry]}')
        #
        # elif msg.topic == 'disco':
        #     print('    Disco message received')
        #     # this will cause the main Platform processing loop to break out
        #     self.processing = False
        #
        # # message with text data.  Note it is actually still binary, so we use .decode() to get the string version
        # else:
        #     print(f'    {msg.payload}')
        #     print(f'    {msg.payload.decode('utf-8')}')



def main():

    my_umpire = Umpire()
    my_umpire.run()

if __name__ == '__main__':
    main()