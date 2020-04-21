load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "impl",
    srcs = ["impl.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store:interface",
        "//xlab/data/store:key",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "impl_test",
    srcs = ["impl_test.py"],
    deps = [
        ":impl",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store:interface",
        "//xlab/net/proto:testing",
        requirement("absl-py"),
        requirement("protobuf"),
    ],
)
