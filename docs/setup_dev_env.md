# Set Up Development Environment

1. Install bazel from bazel.build. The easiest way on Mac OS is to use [Homebrew](https://docs.bazel.build/versions/master/install-os-x.html#install-on-mac-os-x-homebrew).

2. Install [direnv](https://direnv.net/). In particular, add [this snippet](https://github.com/direnv/direnv/wiki/Python#venv-stdlib-module) to support the use of `venv`.
   Note: using vim to add the snippet to your ~/.config/direnv/direnvrc
         vim command to use: "i" -> copy&paste -> "ESC" -> ":wq";

3. Hook direnv into your shell (https://direnv.net/docs/hook.html). 
   Note: cd into your xlab project directory and do "direnv allow";
         Using vim to add eval "$(direnv hook bash)" to ~/.bashrc, then do "source ~/.bashrc" to enable the file.

4. Check your direnv being successfully installed or not.
   try: "which python" and then "python --version";
        "ls -a" (list all the dir including hidden file) then "cat .envrc"


5. Try build and test the codebase:

```sh
$ bazel build //xlab/...
$ bazel test //xlab/...
```
  if you have error like " Xcode version must be specified to use an Apple CROSSTOOL.", try ->
'''
bazel clean --expunge 
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license
bazel clean --expunge
'''

6. Also install the dev tools:

```sh
$ pip install -r requirements-dev.txt
```
useful link for yapf: https://github.com/google/yapf/issues/631
