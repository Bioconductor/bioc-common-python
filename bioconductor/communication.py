import datetime
import logging
import mechanize
import sys

log = logging.getLogger("bioconductor.common")

# log.basicConfig(format='%(levelname)s: %(asctime)s %(filename)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p',
#                     level=log.DEBUG)

from stompy import Stomp
import stomp

# Modules created by Bioconductor
from bioconductor.config import ACTIVEMQ_USER
from bioconductor.config import ACTIVEMQ_PASS
from bioconductor.config import BROKER
from bioconductor.config import CONFIG_ENVIRONMENT
         

stompHost = BROKER['host']
stompPort = BROKER['port']

def getOldStompConnection():
    try:
        log.debug("Attempting to open connection to ActiveMQ at '%s:%s'.",
            stompHost,stompPort)
        # Connect using the old model
        stompClient = Stomp(stompHost, stompPort)
        if (CONFIG_ENVIRONMENT == "production"):
            log.debug("Not attempting authentication")
            stompClient.connect()
        else:
            log.debug("Attempting authentication with user: '%s'.", ACTIVEMQ_USER)
            stompClient.connect(username=ACTIVEMQ_USER, password=ACTIVEMQ_PASS)
        log.debug("Stomp connection established.")
    except:
        log.error("Cannot connect to Stomp at '%s:%s'.", stompHost, stompPort)
        raise
    
    return stompClient

def getNewStompConnection(listenerName, listenerObject):
    try:
        log.debug("Attempting to open connection to ActiveMQ at '%s:%s'.",
            stompHost, stompPort)
        stompClient = stomp.Connection([(stompHost, stompPort)])
        
        stompClient.set_listener(listenerName, listenerObject)
        stompClient.start()
                
        if (CONFIG_ENVIRONMENT == "production"):
            log.debug("Not attempting authentication")
            stompClient.connect()
        else:
            log.debug("Attempting authentication with user: '%s'.", ACTIVEMQ_USER)
            stompClient.connect(username=ACTIVEMQ_USER, password=ACTIVEMQ_PASS)
        log.debug("Stomp connection established.")
    except:
        log.error("Cannot connect to Stomp at '%s:%s'.", stompHost, stompPort)
        raise
    
    return stompClient
