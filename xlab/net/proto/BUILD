load("@rules_python//python:defs.bzl", "py_library")
load("@remote_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "testing",
    srcs = ["testing.py"],
    srcs_version = "PY3",
    deps = [
        requirement("protobuf"),
    ],
)
