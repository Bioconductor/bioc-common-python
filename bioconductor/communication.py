import datetime
import logging
import mechanize
import sys

log = logging.getLogger("bioconductor.common")

# log.basicConfig(format='%(levelname)s: %(asctime)s %(filename)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p',
#                     level=log.DEBUG)

import boto
import boto.sqs
from boto.sqs.message import Message

# Modules created by Bioconductor
from bioconductor.config import ACTIVEMQ_USER
from bioconductor.config import ACTIVEMQ_PASS
from bioconductor.config import BROKER
from bioconductor.config import CONFIG_ENVIRONMENT
from bioconductor.config import AWS

aws_region = AWS['region']
aws_access_key = AWS['access_key']
aws_secret_key = AWS['secret_key']


class QueueWatcher:
    seen = []
    conn = None
    queue = None

    def __init__(self, qname):
        self.conn = boto.sqs.connect_to_region(aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key)
        self.queue = self.conn.get_queue(qname)

    def poll(self):
        m = self.queue.read()
        if m is None:
            return(None)
        if m.id in self.seen:
            return(None)
        else:
            self.seen.append(m.id)
            return(m.get_body())

class MessageSender:

    queue = None
    conn = None

    def __init__(self, qname):
        self.conn = boto.sqs.connect_to_region(aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key)
        self.queue = self.conn.get_queue(qname)

    # use different queues?
    def send(self, body):
        m = Message()
        m.set_body(body)
        self.queue.write(m)
