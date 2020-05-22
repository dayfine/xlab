load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "time_util",
    srcs = ["time_util.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        requirement("protobuf"),
    ],
)
