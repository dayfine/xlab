load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//xlab:internal"])

py_library(
    name = "time",
    srcs = ["time.py"],
    srcs_version = "PY3",
)

py_test(
    name = "time_test",
    srcs = ["time_test.py"],
    srcs_version = "PY3",
    deps = [
        ":time",
        requirement("absl-py"),
    ],
)
