import sys

def get_publisher(publisher_name):
    publisher_name = str(publisher_name)
    _module, _class = publisher_name.rsplit('.', 1)

    try:
        return getattr(
            __import__(
                _module,
                globals=globals(),
                locals=locals(),
                fromlist=[_class],
                level=0
            ),
            _class
        )
    except ImportError, e:
        print >> sys.stderr, '\t\t{}, skipping'.format(e.message)
        return None
    except AttributeError, e:
        print >> sys.stderr, '\t\t{}, skipping'.format(e.message)
        return None

from api.common import CONFIG

def publish_score_event(type, data):
    publishers = CONFIG.get('integration', {}).get('publishers', {})
    for publisher_name in publishers.keys():
        publisher_cls = get_publisher(publisher_name)

        if publisher_cls is None:
            continue

        publisher = publisher_cls(publishers.get(publisher_name))

        publisher.send_score_event(type, data)

def publish_tag_device(data):
    publishers = CONFIG.get('integration', {}).get('publishers', {})
    for publisher_name in publishers.keys():
        publisher_cls = get_publisher(publisher_name)

        if publisher_cls is None:
            continue

        publisher = publisher_cls(publishers.get(publisher_name))

        publisher.publish_tag_device(data)

def request_device_info(ip):
    publishers = CONFIG.get('integration', {}).get('publishers', {})

    """for publisher_name in publishers.keys():
        publisher_cls = get_publisher(publisher_name)

        if publisher_cls is None:
            continue

        publisher = publisher_cls(publishers.get(publisher_name))

        result = publisher.request_device_info(ip)

        if result is not None:
            return result"""

    return (
        {
            'CurrentFlow': {
                'local_port': 443,
                'local_ip': '0.0.0.0',
                'remote_ip': '0.0.0.0',
                'remote_port': 0,
                'status': 'LISTENING',
                'user_id': 'S-1-5-18',
                'user': 'NT AUTHORITY\SYSTEM'
            }
        },
        {
            'CurrentFlow': {
                'local_port': 3180,
                'local_ip': '10.219.100.155',
                'remote_ip': '10.219.100.155',
                'remote_port': 49851,
                'status': 'ESTABLISHED',
                'user_id': 'S-1-5-80-3880718306-3832830129-1677859214-2598158968-1052248003',
                'user': 'NT SERVICE\MSSQLSERVER'
            }
        },
    )
