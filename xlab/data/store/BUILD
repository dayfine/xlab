load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "interface",
    srcs = ["interface.py"],
    srcs_version = "PY3",
    deps = [
        ":units",
        "//xlab/data/proto:data_entry_py_pb2",
    ],
)

py_library(
    name = "impl_test_factory",
    testonly = True,
    srcs = ["impl_test_factory.py"],
    deps = [
        ":interface",
        ":key",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto/testing:compare",
        "//xlab/net/proto/testing:parse",
        requirement("absl-py"),
        requirement("protobuf"),
    ],
)

py_library(
    name = "key",
    srcs = ["key.py"],
    srcs_version = "PY3",
    deps = [
        ":interface",
        ":units",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
    ],
)

py_test(
    name = "key_test",
    srcs = ["key_test.py"],
    deps = [
        ":key",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        requirement("absl-py"),
    ],
)

py_library(
    name = "units",
    srcs = ["units.py"],
    srcs_version = "PY3",
)
