import logging
import logging.config
import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handlers import stations, incidents

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'tornado': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'ROOT': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': False 
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def make_app():
    return Application([
        url(r'/stations', stations.StationCollection),
        url(r'/stations/<id>', stations.StationEntry),
        url(r'/incidents', incidents.IncidentCollection),
        url(r'/incidents/<id>', incidents.IncidentEntry)])


def main():
    app = make_app()
    server = HTTPServer(app)
    server.bind(8888)
    server.start(0)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
