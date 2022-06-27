load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "types",
    srcs = glob([
        "src/**/*.rs",
    ]),
    crate_name = "trading_system",
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/security/id:security_id",
        "//xlab/trading/order",
    ],
)
