import ConfigParser


def config():
    config = ConfigParser.RawConfigParser()
    config.readfp(open('/etc/fire_api/fire_api.conf'))
    return config

