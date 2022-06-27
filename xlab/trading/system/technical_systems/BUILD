load("@rules_rust//rust:defs.bzl", "rust_library")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "technical_systems",
    srcs = glob([
        "src/**/*.rs",
    ]),
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/data/market_data:price_provider",
        "//xlab/data/technical_indicator",
        "//xlab/security/id:security_id",
        "//xlab/trading/system/types",
    ],
)
