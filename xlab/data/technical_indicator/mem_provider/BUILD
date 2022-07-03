load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "mem_provider",
    srcs = glob([
        "src/**/*.rs",
    ]),
    crate_name = "mem_technical_indicator_provider",
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/base/status",
        "//xlab/data/technical_indicator/types",
        "//xlab/security/id:security_id",
    ],
)

rust_test(
    name = "mem_provider_test",
    crate = ":mem_provider",
)
