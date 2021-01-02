from concurrent import futures

from absl import app
from absl import flags
from absl import logging
import grpc
from grpc_reflection.v1alpha import reflection

from xlab.trading.order.proto import placer_pb2, placer_pb2_grpc

FLAGS = flags.FLAGS


class TradeOrderPlacer(placer_pb2_grpc.TradeOrderPlacerServicer):

    def __init__(self):
        pass

    def PlaceOrder(self, request, context):
        print('hello world')

    def UpdateOrder(self, request, context):
        pass

    def ListOpenOrders(self, request, context):
        pass

    def CancelOrder(self, request, context):
        pass


def main(argv):
    del argv  # Unused.

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    placer_pb2_grpc.add_TradeOrderPlacerServicer_to_server(
        TradeOrderPlacer(), server)
    SERVICE_NAMES = (
        placer_pb2.DESCRIPTOR.services_by_name['TradeOrderPlacer'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(main)
