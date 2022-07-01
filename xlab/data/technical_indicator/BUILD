load("@rules_rust//rust:defs.bzl", "rust_library")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "technical_indicator",
    srcs = glob([
        "src/**/*.rs",
    ]),
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/base/status",
        "//xlab/security/id:security_id",
    ],
)
