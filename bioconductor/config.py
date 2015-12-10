# A simple configuration module to reduce duplication.

import os
import platform
import logging
import ConfigParser

logging.basicConfig(format='%(levelname)s: %(asctime)s %(filename)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

logging.debug("Loading configuration")

P_EXTENSION = '.properties'
GLOBAL_PROPERTIES_FILE = os.path.join(os.getcwd(), 'bioconductor' + P_EXTENSION)

def readFile(filename):
    if (os.path.isfile(filename) and os.access(filename, os.R_OK)):
        return True
    else:
        return False

if not readFile(GLOBAL_PROPERTIES_FILE):
    errMsg = "Global properties file '{filename}' is missing or unreadable.  " \
    "Can not continue.".format(filename = GLOBAL_PROPERTIES_FILE)
    logging.error(errMsg)
    raise Exception(errMsg)
    
# Parse and read the file
globalConfigParser = ConfigParser.RawConfigParser()
globalConfigParser.read(GLOBAL_PROPERTIES_FILE)

CONFIG_ENVIRONMENT = globalConfigParser.get('Environment', 'environment');
ENVIRONMENT_PROPERTIES_FILE = os.path.join(os.getcwd(), CONFIG_ENVIRONMENT + P_EXTENSION)

if not readFile(ENVIRONMENT_PROPERTIES_FILE):
    errMsg = "A properties file '{filename}' is required to configure the environment.  "\
    "Can not continue.".format(filename = ENVIRONMENT_PROPERTIES_FILE)
    logging.error(errMsg)
    raise Exception(errMsg)

logging.debug("Environment is set to: '{env}'.".format(env = CONFIG_ENVIRONMENT))

# Parse and read the environment specific configuration
envSpecificConfigParser = ConfigParser.RawConfigParser()
envSpecificConfigParser.read(ENVIRONMENT_PROPERTIES_FILE)

# FIXME: Rather than attempting to read the same properties in any environment,
#           it'd be much better if the config module's constructor (or factory) 
#           offered a callback mechanism, to load the properties file and then
#           dispatch to environment specific functionality.

# Only used in the packagebuilder for now (we need to adjust it's properties)
BUILD_NODES = envSpecificConfigParser.get('Properties', 'builders').split(",")
BROKER = {
    "host": envSpecificConfigParser.get('Properties', 'stomp.host'),
    "port": int(envSpecificConfigParser.get('Properties', 'stomp.port'))
}
logging.info("The following build nodes are enabled: %s.", BUILD_NODES)
ACTIVEMQ_USER=  envSpecificConfigParser.get('Properties', 'activemq.username') #.rstrip('\n')
ACTIVEMQ_PASS = envSpecificConfigParser.get('Properties', 'activemq.password') #.rstrip('\n')

BIOC_VERSION = globalConfigParser.get('UniversalProperties', 'bbs.bioc.version')

# TODO: Consider a better way to determine this
BIOC_R_MAP = {"2.7": "2.12", "2.8": "2.13", "2.9": "2.14",
    "2.10": "2.15", "2.14": "3.1", "3.0": "3.1",
    "3.1": "3.2", "3.2": "3.2", "3.3": "3.3"}

BUILDER_ID = platform.node().lower().replace(".fhcrc.org","")
BUILDER_ID = BUILDER_ID.replace(".local", "")

ENVIR = {
    'bbs_home': envSpecificConfigParser.get('Properties', 'bbs.home'),
    'bbs_R_home': envSpecificConfigParser.get('Properties', 'bbs.r.home'),
    'bbs_node_hostname': BUILDER_ID,
    'bbs_R_cmd': envSpecificConfigParser.get('Properties', 'bbs.r.cmd'),
    'bbs_Bioc_version': BIOC_VERSION,

    'packagebuilder_home': envSpecificConfigParser.get('Properties', 'packagebuilder.home'),

    'bbs_RSA_key': envSpecificConfigParser.get('Properties', 'bbs.rsa.key'),
    'packagebuilder_RSA_key': envSpecificConfigParser.get('Properties', 'spb.rsa.key'),
    'svn_user': envSpecificConfigParser.get('Properties', 'svn.user'),
    'svn_pass': envSpecificConfigParser.get('Properties', 'svn.user'),
    'tracker_user': envSpecificConfigParser.get('Properties', 'tracker.user'),
    'tracker_pass': envSpecificConfigParser.get('Properties', 'tracker.pass')
}

TOPICS = {
    "jobs": "/topic/buildjobs",
    "events": "/topic/builderevents"
}

HOSTS = {
    'svn': 'https://hedgehog.fhcrc.org',
    'tracker': 'https://tracker.bioconductor.org',
    'bioc': 'https://bioconductor.org'
}


logging.debug("Finished loading configuration.")
