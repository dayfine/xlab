load("@rules_proto//proto:defs.bzl", "proto_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library",
     "py_grpc_library")

package(default_visibility=["//xlab:internal"])

proto_library(
    name="placer_proto",
    srcs=["placer.proto"],
)

py_proto_library(
    name="placer_py_pb2",
    deps=[":placer_proto"],
)

py_grpc_library(
    name="placer_py_grpc",
    srcs=[":placer_proto"],
    deps=[":placer_py_pb2"],
)
