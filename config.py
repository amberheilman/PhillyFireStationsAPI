import ConfigParser


def config():

    config = ConfigParser.RawConfigParser()
    config.readfp(open('/etc/ems_api_config.conf'))
    return config
