load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "start_local_runtime",
    srcs = ["start_local_runtime.py"],
    srcs_version = "PY3",
    deps = [
        ":notebook_deps",
        # Required notebook libraries
        requirement("jupyter_http_over_ws"),
        requirement("notebook"),
        # Other 3rd party libraries
        requirement("altair"),
        requirement("apache-beam"),
        requirement("ipywidgets"),
        requirement("pandas"),
    ],
)

py_library(
    name = "notebook_deps",
    srcs_version = "PY3",
    deps = [
        "//xlab/data:notebook_deps",
        "//xlab/util:notebook_deps",
    ],
)
