load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_rust//proto:proto.bzl", "rust_proto_library")

package(default_visibility = ["//xlab:internal"])

proto_library(
    name = "portfolio_proto",
    srcs = ["portfolio.proto"],
    deps = [
        ":security_proto",
        "@com_google_protobuf//:timestamp_proto",
    ],
)

rust_proto_library(
    name = "portfolio_rust_proto",
    deps = [":portfolio_proto"],
)

proto_library(
    name = "security_proto",
    srcs = ["security.proto"],
)

rust_proto_library(
    name = "security_rust_proto",
    deps = [":security_proto"],
)
