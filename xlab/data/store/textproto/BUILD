load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "textproto",
    srcs = ["textproto.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/store:interface",
        "//xlab/data/store/in_memory",
        "//xlab/util/status:errors",
    ],
)

py_test(
    name = "textproto_test",
    srcs = ["textproto_test.py"],
    deps = [
        ":textproto",
        requirement("absl-py"),
    ],
)
