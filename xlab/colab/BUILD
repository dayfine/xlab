load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "start_local_runtime",
    srcs = ["start_local_runtime.py"],
    srcs_version = "PY3",
    deps = [
        ":notebook_deps",
        requirement("jupyter_http_over_ws"),
        requirement("notebook"),
    ],
)

py_library(
    name = "notebook_deps",
    srcs_version = "PY3",
    deps = [
        "//xlab/data/provider:iex",
        "//xlab/util/status:errors",
    ],
)
