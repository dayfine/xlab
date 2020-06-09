load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "notebook_deps",
    srcs_version = "PY3",
    deps = [
        "//xlab/data/calc",
        "//xlab/data/importer/iex",
        "//xlab/data/pipeline:mongo_util",
        "//xlab/data/pipeline:produce_calc_fn",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/proto:data_type_py_pb2",
        "//xlab/data/store/mongo",
    ],
)
