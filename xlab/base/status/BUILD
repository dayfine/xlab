load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

package(default_visibility = ["//xlab:internal"])

rust_library(
    name = "status",
    srcs = [
        "src/lib.rs",
    ],
    edition = "2021",
)

rust_test(
    name = "status_test",
    crate = ":status",
)
