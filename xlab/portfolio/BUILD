load("@rules_rust//rust:defs.bzl", "rust_library", "rust_test")

rust_library(
    name = "position",
    srcs = [
        "src/position.rs",
    ],
    deps = [
        "//third_party/cargo:approx",
        "//third_party/cargo:protobuf",
        "//xlab/proto:portfolio_rust_proto",
    ],
    edition = "2021",
)

rust_test(
    name = "position_test",
    crate = ":position",
)
