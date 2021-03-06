workspace(name = "xlab")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "com_google_protobuf",
    sha256 = "bf0e5070b4b99240183b29df78155eee335885e53a8af8683964579c214ad301",
    strip_prefix = "protobuf-3.14.0",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v3.14.0.zip"],
)

http_archive(
    name = "com_github_grpc_grpc",
    sha256 = "aec9faf1e957caa9a28001a606f9b08ef5a165de6900b04615a304f0d6e139ca",
    strip_prefix = "grpc-1.34.0",
    urls = ["https://github.com/grpc/grpc/archive/v1.34.0.zip"],
)

http_archive(
    name = "rules_proto",
    sha256 = "602e7161d9195e50246177e7c55b2f39950a9cf7366f74ed5f22fd45750cd208",
    strip_prefix = "rules_proto-97d8af4dc474595af3900dd85cb3a29ad28cc313",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
        "https://github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
    ],
)

http_archive(
    name = "rules_python",
    sha256 = "140630a11671b4a5b5e3f1031ff6a8e63c0740dded9c38af9fad49cf6fad00c1",
    strip_prefix = "rules_python-a16432752ef33b98530f05ca86375b42059b23c0",
    urls = [
        "https://github.com/bazelbuild/rules_python/archive/a16432752ef33b98530f05ca86375b42059b23c0.zip",
    ],
)

http_archive(
    name = "io_bazel_rules_rust",
    sha256 = "173e522d81354ab6d2757e7ef1b6d32ac5a86bf70b93af44864f5ccece509e75",
    strip_prefix = "rules_rust-149400c0fb94f872ff6095e544ad879fa201757f",
    urls = [
        "https://github.com/bazelbuild/rules_rust/archive/149400c0fb94f872ff6095e544ad879fa201757f.tar.gz",
    ],
)

http_archive(
    name = "bazel_skylib",
    sha256 = "9a737999532daca978a158f94e77e9af6a6a169709c0cee274f0a4c3359519bd",
    strip_prefix = "bazel-skylib-1.0.0",
    url = "https://github.com/bazelbuild/bazel-skylib/archive/1.0.0.tar.gz",
)

register_toolchains("//:py_toolchain")

# ================================================================
# Proto extensions
# ================================================================
load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@com_github_grpc_grpc//bazel:grpc_extra_deps.bzl", "grpc_extra_deps")

grpc_extra_deps()

# ================================================================
# Proto extensions
# ================================================================
load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

load(
    "@rules_proto//proto:repositories.bzl",
    "rules_proto_dependencies",
    "rules_proto_toolchains",
)

rules_proto_dependencies()

rules_proto_toolchains()

# ================================================================
# Python extensions
# ================================================================
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "py_deps",
    requirements = "//:requirements.txt",
)

# ================================================================
# Rust extensions
# ================================================================
load("@io_bazel_rules_rust//rust:repositories.bzl", "rust_repositories")

rust_repositories()

load("@io_bazel_rules_rust//:workspace.bzl", "bazel_version")

bazel_version(name = "bazel_version")

load("@io_bazel_rules_rust//proto:repositories.bzl", "rust_proto_repositories")

rust_proto_repositories()

load("//third_party/cargo:crates.bzl", "raze_fetch_remote_crates")

raze_fetch_remote_crates()
