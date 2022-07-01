load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "technical_systems",
    srcs = glob([
        "src/**/*.rs",
    ]),
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/base/status",
        "//xlab/data/technical_indicator",
        "//xlab/security/id:security_id",
        "//xlab/trading/order",
        "//xlab/trading/system/types",
    ],
)

rust_test(
    name = "technical_systems_test",
    crate = ":technical_systems",
    deps = [
      "//third_party/cargo:mockall",
    ]
)
