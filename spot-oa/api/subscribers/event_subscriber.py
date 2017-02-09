import base64
import json
import logging
import os
import sys
import urllib3

from dxlclient.broker import Broker
from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig

# Add parent and current dirs
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))

from common import CONFIG, logger
from epo import client as epo_client

# EPO Information
# EPO Information
EPO_HOST = CONFIG['integration']['epo']['host']
EPO_PORT = CONFIG['integration']['epo']['port']
EPO_USER = CONFIG['integration']['epo']['user']
EPO_PASS = CONFIG['integration']['epo']['password']
epo = epo_client(EPO_HOST, EPO_PORT, EPO_USER, EPO_PASS)

OSC_HOST = CONFIG['integration']['osc']['host']
OSC_USER = CONFIG['integration']['osc']['user'] 
OSC_PASS = CONFIG['integration']['osc']['password']
OSC_MAP = CONFIG['integration']['osc']['resources']

DXL_CONFIG =  CONFIG['integration']['publishers']['api.integrators.dxl.SpotDxlClient']

brokers = []
for broker_config in DXL_CONFIG.get('Brokers', tuple()):
    brokers.append(Broker(
        host_name=broker_config['hostname'],
        unique_id=broker_config.get('id', broker_config['hostname']),
        ip_address=broker_config.get('ip'),
        port=broker_config.get('port', 8883)
    ))

CONN_CONFIG = DXL_CONFIG.get('Connection', {})
CERTS_CONFIG = DXL_CONFIG['Certs']
dxl_config = DxlClientConfig(
    broker_ca_bundle=CERTS_CONFIG['BrokerCertChain'],
    cert_file=CERTS_CONFIG['CertFile'],
    private_key=CERTS_CONFIG['PrivateKey'],
    brokers=brokers
)

# Sample topic to fire Events on
if len(sys.argv)>1:
    _type = sys.argv[1]
else:
    _type = 'netflow'

SCORE_EVENT_TOPIC = '/apache/spot/{}/score'.format(_type)
TAG_EVENT_TOPIC = '/apache/spot/dxl/tag'

# Sample Event Subscriber
try:
    logger.info("Event Subscriber - Ctrl + C to exit")

    # Initialize DXL client using our configuration
    logger.info("Event Subscriber - Creating DXL Client")
    with DxlClient(dxl_config) as client:

        # Connect to DXL Broker
        logger.info("Event Subscriber - Connecting to Broker")
        client.connect()

        # Event callback class to handle incoming DXL Events
        class TagEventCallback(EventCallback):
            def on_event(self, event):
                # Extract information from Event payload, in this sample we expect it is UTF-8 encoded
                logger.info("Event Subscriber - Event received:\n   Topic: %s\n   Payload: %s",
                            event.destination_topic, event.payload.decode())

                # Build dictionary from the event payload
                event_dict = json.loads(event.payload.decode())

                if event_dict.get('target', '').lower()=='epo':
                    self.on_epo_event(event_dict)
                elif event_dict.get('target', '').lower()=='osc':
                    self.on_osc_event(event_dict)

            def on_epo_event(self, event_dict):
		names = []
		for ip in [str(event_dict[key]) for key in ['srcIp', 'dstIp'] if event_dict.has_key(key) and event_dict.get(key)!='']:
		    object_name = OSC_MAP['devices'].get(ip, {}).get('name')


                    if object_name is None:
                        logger.warn('Object name not found for {}'.format(ip))
                        continue

                    names.append(object_name)

                if len(names)==0:
                    return

                try:
                    # Build command
                    command = 'system.applyTag'
                    req_dict = {
                        'names': ','.join(names),
                        'tagName': event_dict.get('tag', 'BLOCK')
                    }

                    print command, req_dict

                    # Execute the ePO Remote Command
                    result = epo.run(command, **req_dict)
                except Exception as ex:
                    # Send error response
                    logger.error(str(ex))

            def on_osc_event(self, event_dict):
                try:
                    osc_scope = 'globalroot-0'
                    OSC_URL_TPL = '{}/api/2.0/services/securitygroup/{}/members/{}?failIfExists=false'

                    group_id = OSC_MAP['groups'].get(event_dict.get('tag'))

                    if group_id is None:
                        logger.warn('Invalid group id: {}'.format(event_dict.get('tag')))
                        return

                    for ip in [str(event_dict[key]) for key in ['srcIp', 'dstIp'] if event_dict.has_key(key)]:
                        logger.info('Adding {} as member of {}'.format(ip, event_dict.get('tag')))

                        object_id = OSC_MAP['devices'].get(ip, {}).get('objectId')

                        if object_id is None:
                            logger.warn('Object id not found for {}'.format(ip))
                            continue

                        http = urllib3.PoolManager()

                        osc_endpoint = OSC_URL_TPL.format(OSC_HOST, group_id, object_id)
                        logger.debug('OSC Add member endpoint'.format(osc_endpoint))

                        auth_token = base64.b64encode('{}:{}'.format(OSC_USER, OSC_PASS))
                        r = http.request(
                            'PUT',
                            osc_endpoint,
                            headers={
                                'Accept': 'application/json',
                                'Authorization': 'Basic {}'.format(auth_token)
                            }
                        )

                        if r.status == 200:
                            logger.info('{} has been added to security group ({})'.format(ip, group_id))
                        else:
                            logger.warn('{} could not be added to security group ({})'.format(ip, group_id))
                except Exception as ex:
                    # Send error response
                    logger.error(str(ex))

        # Add Event callback to DXL client
        callback = TagEventCallback()
        logger.info("Adding Event callback function to Topic: %s", TAG_EVENT_TOPIC)
        client.add_event_callback(TAG_EVENT_TOPIC, callback)

        # Wait for DXL Events
        while True:
            try:
                raw_input()
            except KeyboardInterrupt:
                break

except Exception as e:
    logger.info("Event Subscriber - Exception: %s", e.message)
    exit(1)
