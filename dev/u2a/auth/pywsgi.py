from gevent import monkey
from gevent.pywsgi import WSGIServer
from app import app, init

monkey.patch_all()

init()
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
