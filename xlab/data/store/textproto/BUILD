load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "store",
    srcs = ["store.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/data/store",
        "//xlab/data/store/in_memory",
        "//xlab/util/status:errors",
        requirement("absl-py"),
        requirement("protobuf"),
    ],
)

py_test(
    name = "store_test",
    srcs = ["store_test.py"],
    deps = [
        ":textproto",
        "//xlab/data/store:impl_test_factory",
        requirement("absl-py"),
    ],
)

py_library(
    name = "textproto",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":store",
    ],
)
