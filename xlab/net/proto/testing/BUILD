load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "compare",
    srcs = ["compare.py"],
    srcs_version = "PY3",
    deps = [
        requirement("protobuf"),
    ],
)

py_library(
    name = "parse",
    srcs = ["parse.py"],
    srcs_version = "PY3",
    deps = [
        requirement("protobuf"),
    ],
)
