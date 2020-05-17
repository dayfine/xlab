load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "calc",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":interface",
        ":registry",
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

py_library(
    name = "registry",
    srcs = ["registry.py"],
    srcs_version = "PY3",
    deps = [
        ":interface",
        "//xlab/data/calc/producers:factories",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "registry_test",
    srcs = ["registry_test.py"],
    srcs_version = "PY3",
    deps = [
        ":registry",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/data/store/in_memory",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)
