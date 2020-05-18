import json

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def do_something(event, context):
    """Do something awesome

    'event' comes from kinesis stream
    """
    log.info(json.dumps(event))
    return event