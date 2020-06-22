load("@rules_proto//proto:defs.bzl", "proto_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")

package(default_visibility = ["//xlab:internal"])

proto_library(
    name = "order_proto",
    srcs = ["order.proto"],
)

py_proto_library(
    name = "order_py_pb2",
    deps = [":order_proto"],
)
