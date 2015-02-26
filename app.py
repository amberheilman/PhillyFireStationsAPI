from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handlers import stations, incidents


def make_app():
    return Application([
        url(r"/stations/", stations.StationCollection),
        url(r'/stations/<id>', stations.StationEntry),
        url(r'/incidents/', incidents.IncidentCollection),
        url(r'/incidents/<id>', incidents.IncidentEntry)])


def main():
    app = make_app()
    app.listen(80)
    IOLoop.current().start()
