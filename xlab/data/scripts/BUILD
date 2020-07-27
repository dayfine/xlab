load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "backfill_calc",
    srcs = ["backfill_calc.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "//xlab/data/pipeline:produce_calc",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/trading/dates:trading_days",
        requirement("absl-py"),
    ],
)

py_binary(
    name = "iex_fetch_all",
    srcs = ["iex_fetch_all.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "//xlab/data/importer/iex",
        "//xlab/data/importer/iex/api:symbols",
        "//xlab/data/store/mongo",
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
