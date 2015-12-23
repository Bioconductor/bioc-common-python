# Platform dependencies
import sys
import logging

# Logging framework
from testify import *

# Stomp dependencies
from stomp.listener import PrintingListener

# Bioconductor dependencies
from bioconductor.communication import getNewStompConnection
from bioconductor.config import BROKER

class CommunicationTestCase(TestCase):

    @class_setup
    def init_the_variable(self):
        self.variable = 0

    @setup
    def increment_the_variable(self):
        self.variable += 1

    def testHostLineEnding(self):
        assert_equal(BROKER['host'].endswith('\n'), False)

    def testConn(self):
        conn = getNewStompConnection('', PrintingListener())
        assert_not_equal(conn, None)

    def testSubscribeToConn(self):
        try:
            stomp = getNewStompConnection('', PrintingListener())
            print "Client is: '%s'" % stomp
        except:
            logging.error("Cannot connect to Stomp")
            raise

        stomp.subscribe(destination="/topic/builderevents", id="StompUnitTest",
                    ack='auto')
        assert_equal(type("conn") is str, True)

    def testPortLineEnding(self):
        assert_equal(type(BROKER['port']) is str, False)

    # def test_the_variable(self):
    #     assert_equal(self.variable, 1)

    # @suite('disabled', reason='ticket #123, not equal to 2 places')
    # def test_broken(self):
    #     # raises 'AssertionError: 1 !~= 1.01'
    #     assert_almost_equal(1, 1.01, threshold=2)

    @teardown
    def decrement_the_variable(self):
        self.variable -= 1

    @class_teardown
    def get_rid_of_the_variable(self):
        self.variable = None

if __name__ == "__main__":
    run()
