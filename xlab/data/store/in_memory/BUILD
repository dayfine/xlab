load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "in_memory",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":store",
    ],
)

py_library(
    name = "store",
    srcs = ["store.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store",
        "//xlab/data/store:key",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "store_test",
    srcs = ["store_test.py"],
    deps = [
        ":in_memory",
        "//xlab/data/store:impl_test_factory",
        requirement("absl-py"),
    ],
)
