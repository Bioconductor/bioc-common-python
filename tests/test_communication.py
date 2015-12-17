from bioconductor.communication import getOldStompConnection
from testify import *
from bioconductor.config import BROKER
import sys

class AdditionTestCase(TestCase):

    @class_setup
    def init_the_variable(self):
        self.variable = 0

    @setup
    def increment_the_variable(self):
        self.variable += 1

    def testHostLineEnding(self):
        assert_equal(BROKER['host'].endswith('\n'), False)

    def testGetOldConn(self):
        conn = getOldStompConnection()
        assert_equal(type(conn) is str, False)

    def testSubscribeToConn(self):
        try:
            stomp = getOldStompConnection()
            print "Client is: '%s'" % stomp
        except:
            logging.error("Cannot connect to Stomp")
            raise

        retVal = stomp.subscribe({'destination': "/topic/builderevents", 'ack': 'client'})
        print "Subscribe retval is: '%s'" % retVal
        sys.stdout.flush()
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
