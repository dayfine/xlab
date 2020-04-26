load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "interface",
    srcs = ["interface.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
    ],
)
