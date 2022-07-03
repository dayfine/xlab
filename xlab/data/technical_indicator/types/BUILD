load("@rules_rust//rust:defs.bzl", "rust_library")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "types",
    srcs = glob([
        "src/**/*.rs",
    ]),
    crate_name = "technical_indicator",
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/base/status",
        "//xlab/security/id:security_id",
    ],
)
