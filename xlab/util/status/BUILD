load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")
load("@remote_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

proto_library(
    name = "error_codes_proto",
    srcs = ["error_codes.proto"],
)

py_proto_library(
    name = "error_codes_py_pb2",
    deps = ["error_codes_proto"],
)

py_library(
    name = "errors",
    srcs = ["errors.py"],
    srcs_version = "PY3",
    deps = [
        ":error_codes_py_pb2",
    ],
)

py_test(
    name = "errors_test",
    srcs = ["errors_test.py"],
    deps = [
        ":error_codes_py_pb2",
        ":errors",
        requirement("absl-py"),
    ],
)
