# Provide resolved rustc locally, due to cargo raze not providing RUSTC env var
# required by the protobuf crate.
load(":rustc_resolve.bzl", "rustc_resolve")
rustc_resolve(
    name = "rustc"
)
"""
cargo-raze workspace build file.

DO NOT EDIT! Replaced on runs of cargo-raze
"""
package(default_visibility = ["//visibility:public"])

licenses([
  "notice" # See individual crates for specific licenses
])
alias(
    name = "approx",
    actual = "@raze__approx__0_3_2//:approx",
)
alias(
    name = "protobuf",
    actual = "@raze__protobuf__1_6_0//:protobuf",
)
