load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "calc",
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
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
    ],
)
