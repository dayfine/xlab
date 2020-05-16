load("@rules_proto//proto:defs.bzl", "proto_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")

package(default_visibility = ["//xlab:internal"])

proto_library(
    name = "data_entry_proto",
    srcs = ["data_entry.proto"],
    deps = [
        "data_type_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

py_proto_library(
    name = "data_entry_py_pb2",
    deps = [":data_entry_proto"],
)

proto_library(
    name = "data_type_proto",
    srcs = ["data_type.proto"],
)

py_proto_library(
    name = "data_type_py_pb2",
    deps = [":data_type_proto"],
)
