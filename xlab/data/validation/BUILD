load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "notebook_deps",
    srcs_version = "PY3",
    deps = [
        ":duplicates",
    ],
)

py_library(
    name = "duplicates",
    srcs = ["duplicates.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        "//xlab/trading/dates:trading_days",
    ]
)

py_test(
    name = "duplicates_test",
    srcs = ["duplicates_test.py"],
    srcs_version = "PY3",
    deps = [
      ":duplicates",
      "//xlab/data/proto:data_entry_py_pb2",
      "//xlab/data/proto:data_type_py_pb2",
      requirement("absl-py"),
      requirement("protobuf"),
      requirement("proto-matcher"),
      requirement("pyhamcrest"),
    ]
)
