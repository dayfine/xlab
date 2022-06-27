load("@rules_rust//rust:defs.bzl", "rust_library")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "price_provider",
    srcs = [
        "src/lib.rs",
        "src/price_provider.rs",
    ],
    crate_name = "price_provider_lib",
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/security/id:security_id",
    ],
)
