load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "server",
    srcs = ["server.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/trading/order/proto:placer_py_pb2",
        "//xlab/trading/order/proto:placer_py_pb2_grpc",
        requirement("absl-py"),
        requirement("grpcio"),
        requirement("grpcio-reflection"),
    ],
)
