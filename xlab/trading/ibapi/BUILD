load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "client",
    srcs = ["client.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/trading/ibapi/mess:message_client",
        "//xlab/trading/ibapi/mess:message_wrapper",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_binary(
    name = "test_app",
    srcs = ["test_app.py"],
    srcs_version = "PY3",
    deps = [
        ":client",
        requirement("absl-py"),
    ],
)
