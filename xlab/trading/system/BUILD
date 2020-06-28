load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "system",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":interface",
    ],
)

py_library(
    name = "interface",
    srcs = ["interface.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/trading/proto:order_py_pb2",
    ],
)
