load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "iex_fetch_all",
    srcs = ["iex_fetch_all.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/importer/iex",
        "//xlab/data/importer/iex:api",
        "//xlab/data/store/mongo",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)

py_binary(
    name = "iex_fetch_data",
    srcs = ["iex_fetch_data.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/importer/iex",
        "//xlab/data/store/textproto",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)

py_binary(
    name = "import_to_mongo",
    srcs = ["import_to_mongo.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store/mongo",
        "//xlab/util/status:errors",
        requirement("absl-py"),
        requirement("protobuf"),
    ],
)
