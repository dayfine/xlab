load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@remote_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "iex",
    srcs = ["iex.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data:provider",
        "//xlab/net/http:requests",
        requirement("absl-py"),
    ],
)

py_test(
    name = "iex_test",
    srcs = ["iex_test.py"],
)
