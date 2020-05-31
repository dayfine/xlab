load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

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
    name = "input_util",
    srcs = ["input_util.py"],
    srcs_version = "PY3",
    deps = [
        ":calc",
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        "//xlab/trading/dates:trading_days",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "input_util_test",
    srcs = ["input_util_test.py"],
    srcs_version = "PY3",
    deps = [
        ":calc",
        ":input_util",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto/testing:compare",
        "//xlab/net/proto/testing:parse",
        "//xlab/util/status:errors",
        requirement("absl-py"),
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
        ":calc",
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
        "//xlab/data/calc/producers:factories",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)
