import logging

log = logging.getLogger("bioconductor.common")

# log.basicConfig(format='%(levelname)s: %(asctime)s %(filename)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p',
#                     level=log.DEBUG)

import stomp

# Modules created by Bioconductor
from bioconductor.config import BROKER

stompHost = BROKER['host']
stompPort = BROKER['port']

def getNewStompConnection(listenerName, listenerObject):
    try:
        log.debug("Attempting to open connection to broker at '%s:%s'.",
            stompHost, stompPort)
        stompClient = stomp.Connection([(stompHost, stompPort)])

        stompClient.set_listener(listenerName, listenerObject)
        stompClient.start()


        stompClient.connect()
        log.debug("Stomp connection established.")
    except:
        log.error("Cannot connect to Stomp at '%s:%s'.", stompHost, stompPort)
        raise

    return stompClient
