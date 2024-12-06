from configparser import ConfigParser
from confluent_kafka import Producer
from loguru import logger
import json


def send_to_kafka(config: ConfigParser, message):
    topic = config["health-monitoring"]["topic"]
    kafka_confs = {
        "bootstrap.servers": config["health-monitoring"]["brokers"],
        "ssl.ca.location": config["health-monitoring"]["ssl_ca_location"],
        "ssl.key.location": config["health-monitoring"]["ssl_key_location"],
        "ssl.key.password": config["health-monitoring"]["ssl_key_password"],
        "ssl.certificate.location": config["health-monitoring"]["ssl_certificate_location"],
        "security.protocol": config["health-monitoring"]["security_protocol"],
    }



    def delivery_report(err, msg):
        if err is not None:
            raise Exception('Message delivery failed: {}'.format(err))
        else:
            logger.debug('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    try:
        p = Producer(kafka_confs)
        p.produce(topic=topic, value=json.dumps(message), on_delivery=delivery_report)
        p.flush()
        return 'Message sent successfully'
    except Exception as e:
        print("Got kafka error ", e)
        raise e
