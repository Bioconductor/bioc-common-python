import datetime
import logging
import mechanize
import sys
import time

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
    retention_period_in_seconds = 60

    def __init__(self, qname):
        self.conn = boto.sqs.connect_to_region(aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key)
        self.queue = self.conn.get_queue(qname)


    def purge_old_messages(self):
        new_seen = []
        current_time = time.time()
        for item in self.seen:
            age = current_time - item[1]
            if age < self.retention_period_in_seconds:
                new_seen.append(item)
        self.seen = new_seen

    def poll(self):
        m = self.queue.read()
        if m is None:
            return(None)
        self.purge_old_messages()
        current_time = time.time()
        tuple = (m.id, current_time,)
        for i in self.seen:
            if i[0] == m.id:
                return(None)
        self.seen.append(tuple)
        return(m.get_body())

class MessageSender:

    queue = None
    conn = None

    def __init__(self, qname):
        self.conn = boto.sqs.connect_to_region(aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key)
        self.queue = self.conn.get_queue(qname)

    def send(self, body):
        m = Message()
        m.set_body(body)
        self.queue.write(m)
