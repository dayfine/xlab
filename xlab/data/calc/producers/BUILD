load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "ema",
    srcs = ["ema.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "//xlab/data/calc:interface",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/data/store",
        "//xlab/net/proto:time_util",
        "//xlab/util/status:errors",
        requirement("pandas"),
    ],
)

py_test(
    name = "ema_test",
    srcs = ["ema_test.py"],
    deps = [
        ":ema",
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/data/store/in_memory",
        "//xlab/net/proto:time_util",
        "//xlab/net/proto/testing:compare",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)

py_library(
    name = "factories",
    srcs = ["factories.py"],
    srcs_version = "PY3",
    deps = [
        ":ema",
        "//xlab/data/proto:data_type_py_pb2",
    ],
)
