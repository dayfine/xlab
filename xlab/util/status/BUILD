load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")

package(default_visibility = ["//xlab:internal"])

proto_library(
    name = "error_codes_proto",
    srcs = ["error_codes.proto"],
)

py_proto_library(
    name = "error_codes_pb2",
    srcs = ["error_codes.proto"],
)

py_library(
    name = "errors",
    srcs = ["errors.py"],
    srcs_version = "PY3",
    deps = [
        ":error_codes_pb2",
    ],
)
