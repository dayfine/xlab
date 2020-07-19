load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "admin",
    srcs = ["admin.py"],
    srcs_version = "PY3",
)

py_library(
    name = "constants",
    srcs = ["constants.py"],
    srcs_version = "PY3",
)

py_library(
    name = "db_client",
    srcs = ["db_client.py"],
    srcs_version = "PY3",
    deps = [
        ":constants",
        requirement("pymongo"),
    ],
)

py_library(
    name = "mongo",
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
        ":constants",
        ":db_client",
        "//xlab/base:time",
        "//xlab/data/converters:mongo",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store",
        "//xlab/data/store:key",
        "//xlab/util/status:errors",
        requirement("pymongo"),
        requirement("protobuf"),
    ],
)

py_test(
    name = "store_test",
    srcs = ["store_test.py"],
    deps = [
        ":mongo",
        "//xlab/data/store:impl_test_factory",
        requirement("absl-py"),
        requirement("mongomock"),
    ],
)
