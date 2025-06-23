import paho.mqtt.client
import sys
import pickle

import Platform

def main():

    my_client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)

    # connect to MQTT broker
    if my_client.connect(host = 'fourbee', port = 1883, keepalive = 60) != 0:
        print('Could not connect to MQTT broker')
        sys.exit(-1)

    # binary message
    platform = Platform.Platform()
    platform.platform_status.location.x = 7
    platform.platform_status.location.y = -9
    platform.platform_status.depth = 9999   # just to confirm the info gets pickled/unpickled correctly
    my_client.publish(topic = 'platform_status', payload = pickle.dumps(platform.platform_status), qos = 0)

    # text message
    my_client.publish(topic = 'general', payload = 'Generic text message', qos = 0)

    my_client.disconnect()


if __name__ == '__main__':
    main()