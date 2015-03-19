import logging
import logging.config

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handlers import stations, incidents

from configuration import config

config = config()
log_file = config.get('logging', 'file')
logging.config.fileConfig(log_file)
logger = logging.getLogger(__name__)

def make_app():
    logger.info('MAKING APPLICATION')
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
