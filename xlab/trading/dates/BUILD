load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "trading_days",
    srcs = ["trading_days.py"],
    data = ["data/us_trading_days.txt"],
    srcs_version = "PY3",
    deps = [
        "//xlab/base:time",
        "@rules_python//python/runfiles",
    ],
)

py_test(
    name = "trading_days_test",
    srcs = ["trading_days_test.py"],
    deps = [
        ":trading_days",
        requirement("absl-py"),
    ],
)
