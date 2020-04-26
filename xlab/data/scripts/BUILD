load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_binary(
    name = "iex_ema",
    srcs = ["iex_ema.py"],
    srcs_version = "PY3",
    deps = [
        "//xlab/data/provider/iex:provider",
        "//xlab/util/status:errors",
        requirement("absl-py"),
    ],
)
