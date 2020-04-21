load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "requests",
    srcs = ["requests.py"],
    srcs_version = "PY3",
    deps = [
        requirement("requests"),
    ],
)
