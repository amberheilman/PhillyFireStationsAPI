import logging
import os

from tornado import gen, web
import queries


logger = logging.getLogger(__name__)


class _BaseHandler(web.RequestHandler):

    @gen.coroutine
    def call_proc(self, proc_name, *args, **kwargs):
        """Wrap the call to the stored proc and provide error handling.

        :param proc_name str: the name of the stored procedure to call
        :param args list: args to pass to `queries.sesion.callproc`
        :param kwargs dict: args to pass to `queries.sesion.callproc`

        :returns: `queries.Results` | None

        """
        try:
            results = yield self.session.callproc(proc_name, *args, **kwargs)
        except Exception as exc:
            raise exc
            
            
            
            # (queries.DataError, queries.IntegrityError) as error:
            # logger.critical('crit')
            # raise
        # web.HTTPError(
                # status_code=400)
            # ,
                # log_message=error,
                # reason={'error':
                     # {'description': error.pgerror.split('\n')[0][8:]}})
        # except Exception as error:
            # print('ERr %s', error)
            # raise web.HTTPError(
                # status_code=500,
                # log_message=error,
                # reason={'error':
                     # {'description': error.pgerror.split('\n')[0][8:]}})

        # logger.debug('Query results: %s' % results)
        # results_dict = results.as_dict() if results else {}
        # results.free()
        raise gen.Return(results)


    def initialize(self):
        if not hasattr(self, 'session'):
            self.session = queries.TornadoSession(os.environ['POSTGRES_URI'])

    @gen.coroutine
    def prepare(self):
        try:
            yield self.session.validate()

        except queries.OperationalError as error:
            logger.error('Error connecting to the database: %s', error)
            raise web.HTTPError(503)

    def options(self, *args, **kwargs):
        """Let the caller know what methods are supported

        :param list args: URI path arguments passed in by Tornado
        :param dict kwargs: URI path keyword arguments passed in by Tornado

        """
        self.set_header('Allow', ', '.join(['GET']))
        self.set_status(204)
        self.finish()
