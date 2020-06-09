# Using Colab local runtime

Based on: https://research.google.com/colaboratory/local-runtimes.html

0. Install the required packages (for CLI access):

```sh
$ pip install -r requirements-dev.txt
```

NOTE: other packages such as `altair`, are included in the [runtime BUILD target](./BUILD).


1. Check `jupypter` points to the right binary:

```sh
$ which jupyter
```

This should point to the jupyter binary under `xlab/.venv/bin/jupyter`.

2. Check if the necessary extensions have been enabled

```sh
$ jupyter nbextension list
$ jupyter serverextension list
```

Enable them if necessary.

```sh
$ jupyter nbextension enable --py widgetsnbextension  --sys-prefix # for ipywidgets
$ jupyter serverextension enable --py jupyter_http_over_ws --sys-prefix
```

3. Start the local jupyter server with the xlab dependencies:

```sh
$ xlab/colab/start_local_runtime.sh
```

4. Open the Colab
