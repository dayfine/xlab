load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "mongo_util",
    srcs = ["mongo_util.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/converters:mongo",
        "//xlab/data/store/mongo:constants",
        requirement("apache-beam"),
    ],
)

py_test(
    name = "mongo_util_test",
    srcs = ["mongo_util_test.py"],
    srcs_version = "PY3",
    tags = [
        # Cannot mock pymongo in beam. Requires local mongo instance.
        "manual",
    ],
    deps = [
        ":mongo_util",
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        requirement("apache-beam"),
        requirement("absl-py"),
        requirement("pymongo"),
    ],
)

py_binary(
    name = "produce_calc",
    srcs = ["produce_calc.py"],
    srcs_version = "PY3",
    deps = [
        ":mongo_util",
        ":produce_calc_fn",
        "//xlab/base:time",
        "//xlab/data/calc:registry",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        "//xlab/trading/dates:trading_days",
        requirement("absl-py"),
        requirement("apache-beam"),
    ],
)

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
        "//xlab/trading/dates:trading_days",
        requirement("absl-py"),
        requirement("apache-beam"),
        requirement("protobuf"),
    ],
)
