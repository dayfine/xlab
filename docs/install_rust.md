# Install Rust on new machines

1. Install Rust & Cargo
   
   ```sh
   $ curl https://sh.rustup.rs -sSf | sh
   ```

   If needed, reload current shell:
    
   ```sh
   $  source $HOME/.cargo/env
   ```

1. Install Cargo Raze


   ```sh
   $ cargo install cargo-raze
   ```

   This might require installing `pkg-config` and `openssl` if it doesn't exist

   ```sh
   $ brew install pkg-config
   $ brew install openssl
   ```

1. If everything works, Rust code can compile and be tested:

   ```sh
   $ blaze test //xlab/...
   ```