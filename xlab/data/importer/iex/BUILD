load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "api",
    srcs = ["api.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/net/http:requests",
    ],
)

py_library(
    name = "iex",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":importer",
    ],
)

py_library(
    name = "importer",
    srcs = ["importer.py"],
    srcs_version = "PY3",
    deps = [
        ":api",
        "//xlab/data/importer",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
    ],
)

py_test(
    name = "importer_test",
    srcs = ["importer_test.py"],
    deps = [
        ":importer",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto/testing:compare",
        requirement("absl-py"),
        requirement("requests"),
    ],
)
