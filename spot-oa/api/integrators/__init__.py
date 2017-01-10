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
