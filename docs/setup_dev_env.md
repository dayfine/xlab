# Set Up Development Environment

1. Install bazel from bazel.build. The easiest way on Mac OS is to use [Homebrew](https://docs.bazel.build/versions/master/install-os-x.html#install-on-mac-os-x-homebrew).

2. Install [direnv](https://direnv.net/). In particular, add [this snippet](https://github.com/direnv/direnv/wiki/Python#venv-stdlib-module) to support the use of `venv`.

3. Create a `secrets.rc` file on project root. Contact @dayfine to obtain the secrets.

4. Try build and test the codebase:

```sh
$ bazel build //xlab/...
$ bazel test //xlab/...
```

5. Also install the dev tools:

```sh
$ pip install -r requirements-dev.txt
```
