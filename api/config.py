import ConfigParser

def get_config():
    config = ConfigParser.ConfigParser()
    config.read('/home/amber/git/config.conf')
    return config
