load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "mongo",
    srcs = ["mongo.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        requirement("protobuf"),
    ],
)
