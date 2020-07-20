load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "base",
    srcs = ["base.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/net/http:requests",
        "//xlab/util/status:errors",
        requirement("requests"),
    ],
)

py_library(
    name = "batch",
    srcs = ["batch.py"],
    srcs_version = "PY3",
    deps = [
        ":base",
    ],
)

py_library(
    name = "symbols",
    srcs = ["symbols.py"],
    srcs_version = "PY3",
    deps = [
        ":base",
    ],
)
