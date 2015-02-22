

import ConfigParser, os
import io

def config():


    config = ConfigParser.RawConfigParser()
    config.readfp(open('/home/amber/git/config.conf'))
    return config
