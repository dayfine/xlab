load("@rules_rust//rust:defs.bzl", "rust_library")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "technical_systems",
    srcs = glob([
        "src/**/*.rs",
    ]),
    aliases = {
        "//xlab/data/market_data:price_provider": "price_provider_lib",
        "//xlab/security/id:security_id": "security_id_lib",
        "//xlab/trading/system/types": "trading_system",
    },
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/data/market_data:price_provider",
        "//xlab/data/technical_indicator",
        "//xlab/security/id:security_id",
        "//xlab/trading/system/types",
    ],
)
