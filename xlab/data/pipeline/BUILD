load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "produce_calc_fn",
    srcs = ["produce_calc_fn.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "//xlab/data/calc",
        "//xlab/data/calc:input_util",
        "//xlab/data/calc:registry",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/util/status:errors",
        requirement("absl-py"),
        requirement("apache-beam"),
    ],
)

py_test(
    name = "produce_calc_fn_test",
    srcs = ["produce_calc_fn_test.py"],
    deps = [
        ":produce_calc_fn",
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        "//xlab/net/proto/testing:parse",
        "//xlab/trading/dates:trading_days",
        requirement("absl-py"),
        requirement("apache-beam"),
    ],
)
