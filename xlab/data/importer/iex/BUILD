load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

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
        "//xlab/base:time",
        "//xlab/data/importer",
        "//xlab/data/importer/iex/api:batch",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/net/proto:time_util",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "importer_test",
    srcs = ["importer_test.py"],
    deps = [
        ":importer",
        "//xlab/base:time",
        "//xlab/data/proto:data_type_py_pb2",
        requirement("absl-py"),
        requirement("requests"),
        requirement("proto-matcher"),
        requirement("pyhamcrest"),
    ],
)
