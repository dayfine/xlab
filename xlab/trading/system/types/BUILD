load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "types",
    srcs = glob([
        "src/**/*.rs",
    ]),
    aliases = {
        "//xlab/security/id:security_id": "security_id_lib",
    },
    edition = "2021",
    deps = [
        "//third_party/cargo:chrono",
        "//xlab/security/id:security_id",
        "//xlab/trading/order",
    ],
)
