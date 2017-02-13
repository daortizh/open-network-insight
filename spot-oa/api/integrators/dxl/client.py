from dxlclient.broker import Broker
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event, Request, Message
from dxlmarclient import MarClient

from dxlmarclient.constants import ConditionConstants, OperatorConstants

import json

from api.common import logger

class SpotDxlClient:
    def __init__(self, config):
        self._config = config

    def _get_config(self):
        brokers = []
        for broker_config in self._config.get('Brokers', tuple()):
            brokers.append(Broker(
                host_name=broker_config['hostname'],
                unique_id=broker_config.get('id', broker_config['hostname']),
                ip_address=broker_config.get('ip'),
                port=broker_config.get('port', 8883)
            ))

        CONN_CONFIG = self._config.get('Connection', {})
        CERTS_CONFIG = self._config['Certs']

        dxl_config = DxlClientConfig(
            broker_ca_bundle=CERTS_CONFIG['BrokerCertChain'],
            cert_file=CERTS_CONFIG['CertFile'],
            private_key=CERTS_CONFIG['PrivateKey'],
            brokers=brokers
        )
        dxl_config.connect_retries=CONN_CONFIG.get('retries', 1)
        dxl_config.reconnect_when_disconnected = False

        return dxl_config

    def _create_client(self):
        return DxlClient(self._get_config())

    def send_score_event(self, type, data):
        EVENT_TOPIC = '/apache/spot/{}/score'.format(type)

        # Initialize DXL client using our configuration
        logger.info("Event Publisher - Creating DXL Client")
        with self._create_client() as client:
            logger.info('DXL Publisher - Connecting to Broker')
            try:
                client.connect()
            except:
                logger.error('DXL was not able to stablish a connection')
                return

            logger.info('DXL Publisher - Connected to Broker')
            event = Event(EVENT_TOPIC)

            # Encode string payload as json
            event.payload = json.dumps(data).encode()

            # Publish the Event to the DXL Fabric on the Topic
            logger.info('DXL Publisher - Publishing Event to {}'.format(EVENT_TOPIC))
            client.send_event(event)

    def publish_tag_device(self, data):
        EVENT_TOPIC = '/apache/spot/dxl/tag'

        # Initialize DXL client using our configuration
        logger.info("Event Publisher - Creating DXL Client")
        with self._create_client() as client:
            logger.info('DXL Publisher - Connecting to Broker')
            try:
                client.connect()
            except:
                logger.error('DXL was not able to stablish a connection')
                return

            logger.info('DXL Publisher - Connected to Broker')
            event = Event(EVENT_TOPIC)

            # Encode string payload as json
            event.payload = json.dumps(data).encode()

            # Publish the Event to the DXL Fabric on the Topic
            logger.info('DXL Publisher - Publishing Event to {}'.format(EVENT_TOPIC))
            client.send_event(event)

    def request_device_info(self, ip):
        # Initialize DXL client using our configuration
        logger.info("Request info from MAR - Creating DXL Client")
        with self._create_client() as client:
            try:
                client.connect()
            except:
                logger.error('DXL was not able to stablish a connection')
                return None

            # Create the search
            logger.info("Request info from MAR - Sending search criteria")

            # Create the McAfee Active Response (MAR) client
            mar_client = MarClient(client)
            mar_client.response_timeout = 60

            # Performs the search
            result_context = \
                mar_client.search(
                    projections=[{
                        'name': 'CurrentFlow'
                    },{
                        'name': 'NetworkFlow'
                    }],
                    conditions={
                        ConditionConstants.OR: [{
                            ConditionConstants.AND: [{
                                ConditionConstants.COND_NAME: "HostInfo",
                                ConditionConstants.COND_OUTPUT: "ip_address",
                                ConditionConstants.COND_OP: OperatorConstants.EQUALS,
                                ConditionConstants.COND_VALUE: ip
                            }]
                        }]
                    }
                )

            # Loop and display the results
            if result_context.has_results:
                search_result = result_context.get_results(limit=100)
                print "Results:"
                for item in search_result["items"]:
                    print "    " + str(item["output"])
                return [item['output'] for item in search_result['items']]

            else:
                return None
