# A simple configuration module to reduce duplication.

import os
import os.path
import platform
import logging
import ConfigParser

# log.basicConfig(format='%(levelname)s: %(asctime)s %(filename)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p',
#                     level=log.DEBUG)

log = logging.getLogger("bioconductor.common")
log.debug("Loading configuration")

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
    log.error(errMsg)
    raise Exception(errMsg)

# Parse and read the file
globalConfigParser = ConfigParser.RawConfigParser()
globalConfigParser.read(GLOBAL_PROPERTIES_FILE)

environment = globalConfigParser.get('Environment', 'environment')
ENVIRONMENT_PROPERTIES_FILE = os.path.join(os.getcwd(), environment + P_EXTENSION)
# git clone https://github.com/Bioconductor/spb-properties in current directory
# (that's a private repo to hold sensitive info)
SENSITIVE_PROPERTIES_FILE = os.path.join(os.getcwd(), "spb-properties", "spb" + P_EXTENSION)

if not readFile(ENVIRONMENT_PROPERTIES_FILE):
    errMsg = "A properties file '{filename}' is required to configure the environment.  "\
    "Can not continue.".format(filename = ENVIRONMENT_PROPERTIES_FILE)
    log.error(errMsg)
    raise Exception(errMsg)

log.info("Environment is set to: '{env}'.".format(env = environment))

# Parse and read the environment specific configuration
envConfig = ConfigParser.RawConfigParser()
envConfig.read(ENVIRONMENT_PROPERTIES_FILE)

sensitiveConfigParser = ConfigParser.RawConfigParser()
sensitiveConfigParser.read(SENSITIVE_PROPERTIES_FILE)

# FIXME: Rather than attempting to read the same properties in any environment,
#           it'd be much better if the config module's constructor (or factory)
#           offered a callback mechanism, to load the properties file and then
#           dispatch to environment specific functionality.

# Only used in the packagebuilder for now (we need to adjust it's properties)
BUILD_NODES = envConfig.get('Properties', 'builders').lower().split(",")
BROKER = {
    "host": envConfig.get('Properties', 'stomp.host'),
    "port": int(envConfig.get('Properties', 'stomp.port'))
}
log.info("The following build nodes are enabled: %s.", BUILD_NODES)
if envConfig.has_option('Properties', 'activemq.username'):
    ACTIVEMQ_USER = envConfig.get('Properties', 'activemq.username')
else:
    ACTIVEMQ_USER = None
if envConfig.has_option('Properties', 'activemq.password'):
    ACTIVEMQ_PASS = envConfig.get('Properties', 'activemq.password')
else:
    ACTIVEMQ_PASS = None

BIOC_VERSION = globalConfigParser.get('UniversalProperties', 'bbs.bioc.version')

# TODO: Consider a better way to determine this
BIOC_R_MAP = {"2.7": "2.12", "2.8": "2.13", "2.9": "2.14",
              "2.10": "2.15", "2.14": "3.1", "3.0": "3.1",
              "3.1": "3.2", "3.2": "3.2", "3.3": "3.3",
              "3.4": "3.3", "3.5": "3.4", "3.6": "3.4",
              "3.7": "3.5", "3.8": "3.5", "3.9": "3.6",
              "3.10": "3.6", "3.11": "4.0", "3.12": "4.0"}

BUILDER_ID = platform.node().lower().replace(".fhcrc.org","")
BUILDER_ID = BUILDER_ID.replace(".local", "")
BUILDER_ID = BUILDER_ID.replace(".bioconductor.org", "")

BBS_HOME = envConfig.get('Properties', 'bbs.home')

ENVIR = {
    'bbs_Bioc_version': BIOC_VERSION,
    'bbs_RSA_key': envConfig.get('Properties', 'bbs.rsa.key'),
    'bbs_R_cmd': envConfig.get('Properties', 'bbs.r.home') + "bin/R",
    'bbs_R_home': envConfig.get('Properties', 'bbs.r.home'),
    'bbs_central_rhost': envConfig.get('Properties','bbs.central.rhost'),
    'bbs_central_ruser': envConfig.get('Properties','bbs.central.ruser'),
    'bbs_home': BBS_HOME,
    'bbs_mode': envConfig.get('Properties','bbs.mode'),
    'bbs_node_hostname': BUILDER_ID,
    'bbs_python_cmd': envConfig.get('Properties','bbs.python.cmd'),
    'bbs_rsync_cmd': envConfig.get('Properties','bbs.rsync.cmd'),
    'bbs_ssh_cmd': envConfig.get('Properties','bbs.ssh.cmd'),
    'bbs_svn_cmd': envConfig.get('Properties','bbs.svn.cmd'),
    'bbs_tar_cmd': envConfig.get('Properties','bbs.tar.cmd'),
    'bbs_curl_cmd': envConfig.get('Properties','bbs.curl.cmd'),
    'bbs_lang': envConfig.get('Properties','bbs.lang'),

    'spb_RSA_key': envConfig.get('Properties', 'spb.rsa.key'),
    'spb_home': envConfig.get('Properties', 'spb.home'),
    'spb_staging_url': envConfig.get('Properties', 'spb.staging.url'),

    'github_issue_repo': envConfig.get('Properties', 'github.issue.repo'),

    'r_check_environ': envConfig.get('Properties', 'r.check.environ'),

    'log_level': envConfig.get('Properties', 'log.level'),
    'log_level_builder': envConfig.get('Properties', 'log.level.builder'),
    'log_level_server': envConfig.get('Properties', 'log.level.server'),
    'timeout_limit': envConfig.get('Properties', 'timeout.limit'),

    'svn_pass': sensitiveConfigParser.get('Sensitive', 'svn.user'),
    'svn_user': sensitiveConfigParser.get('Sensitive', 'svn.user'),
    'github_token': sensitiveConfigParser.get('Sensitive', 'github.token'),
    'bioc_devel_password': sensitiveConfigParser.get('Sensitive', 'bioc.devel.password')
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


log.info("Finished loading configuration.")
