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
    name = "provider",
    srcs = ["provider.py"],
    srcs_version = "PY3",
    deps = [
        ":api",
        "//xlab/data/proto:data_entry_py_pb2",
        "//xlab/data/provider:interface",
    ],
)

py_test(
    name = "provider_test",
    srcs = ["provider_test.py"],
    deps = [
        ":provider",
        "//xlab/net/proto/testing:compare",
        requirement("absl-py"),
        requirement("requests"),
    ],
)
