load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "message_client",
    srcs = ["message_client.py"],
    srcs_version = "PY3",
    deps = [
        ":messages",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_library(
    name = "messages",
    srcs = ["messages.py"],
    srcs_version = "PY3",
)

py_library(
    name = "message_wrapper",
    srcs = ["message_wrapper.py"],
    srcs_version = "PY3",
    deps = [
        ":messages",
        requirement("ibapi"),
        requirement("rx"),
    ],
)
