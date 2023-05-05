from concurrent import futures

import grpc

from auth.grpcs.user_pb2_grpc import userServicer, add_userServicer_to_server
from auth.grpcs.user_pb2 import Roles
from app import app, init
from auth.services.user import UserService
from auth.core.config import GRPC_SERVER_PORT, GRPC_SERVER_THREADS, GRPC_SERVER_HOST


class User(userServicer):
    def whois(self, request, context):
        with app.app_context():
            srv = app.service(UserService)
            return Roles(roles=srv.whois(user_data={}, jwt=request.jwt))


if __name__ == '__main__':
    init(app)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_SERVER_THREADS))
    add_userServicer_to_server(User(), server)
    server.add_insecure_port('{}:{}'.format(GRPC_SERVER_HOST, GRPC_SERVER_PORT))
    server.start()
    server.wait_for_termination()
