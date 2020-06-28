# Cargo Vendored Dependencies

See instructions of <https://github.com/google/cargo-raze> on how files in this directory are created.

## Adding New Crates

- Add the crates wanted to the `[dependencies]` section of `Cargo.toml`.
- In the workspace root, run `make raze` (See `Makefile`).
