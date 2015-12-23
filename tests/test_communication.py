# Platform dependencies
import sys
import logging

# Logging framework
from testify import *

# Stomp dependencies
from stomp.listener import ConnectionListener

# Bioconductor dependencies
from bioconductor.communication import getNewStompConnection
from bioconductor.config import BROKER

# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
log = logging.getLogger("CommunicationTestCase")
log.addHandler(logging.StreamHandler())
log.propagate = False
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())
log.removeHandler(log.handlers[0])

rootLogger = logging.getLogger()
fh = logging.FileHandler('TestingRoot.log')
fh.setLevel(logging.INFO)
rootLogger.addHandler(fh)
rootLogger.disabled = True
rootLogger.removeHandler(rootLogger.handlers[0])


class CommunicationTestCase(TestCase):

    @class_setup
    def init_the_variable(self):
        self.stompClient = None

    @setup
    def increment_the_variable(self):
        try:
            self.stompClient = getNewStompConnection('', ConnectionListener())
        except:
            log.error('''
Cannot connect to Stomp; make sure you're running a local ActiveMQ instance.
You can start a docker container with ActiveMQ using the following :
`docker run --name='activemq' -d -p 8161:8161 -p 61616:61616 -p 61613:61613 rmohr/activemq:5.10.0`
'''
            )
            sys.exit(1)
        
    def testHostIsString(self):
        assert_equal(type(BROKER['host']) is str, True)

    def testConnectionIsCreated(self):
        assert_not_equal(self.stompClient, None)

    def testSubscribing(self):
        self.stompClient.subscribe(destination="/topic/builderevents", id="StompUnitTest",
                    ack='auto')
        log.info("Subscription is working")
    
    def testConnectionType(self):
        assert_equal(type("self.stompClient") is str, True)

    @teardown
    def decrement_the_variable(self):
        self.stompClient = None

    @class_teardown
    def get_rid_of_the_variable(self):
        log.info("Finished all tests")
        
if __name__ == "__main__":
    run()
