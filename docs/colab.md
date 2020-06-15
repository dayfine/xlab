# Using Colab local runtime

Based on: <https://research.google.com/colaboratory/local-runtimes.html>

0. Install the required packages (for CLI access):

    ```sh
    pip install -r requirements-dev.txt
    ```

    NOTE: other packages such as `altair`, are included in the [runtime BUILD target](./BUILD).

1. Check `jupypter` points to the right binary:

    ```sh
    which jupyter
    ```

    This should point to the jupyter binary under `xlab/.venv/bin/jupyter`.

2. Check if the necessary extensions have been enabled

    ```sh
    jupyter nbextension list
    jupyter serverextension list
    ```

    Enable them if necessary.

    ```sh
    jupyter nbextension enable --py widgetsnbextension  --sys-prefix # for ipywidgets
    jupyter serverextension enable --py jupyter_http_over_ws --sys-prefix
    ```

3. Start the local jupyter server with the xlab dependencies:

    ```sh
    xlab/colab/start_local_runtime.sh
    ```

    > Once the server has started, it will print a message with the initial backend URL used for authentication. Make a copy of this URL as you'll need to provide this in the next step.

    NOTE: Currently config file has to be explicitly specified as a work-around for <https://github.com/dillon-giacoppo/rules_python_external/issues/47.>

4. Open the Colab

    Use the `Github` and load the Colab notebook under `xlab/colab/notebooks` from Github. Make a copy if necessary. After making changes, save the notebook back to Github.

5. Connect to local runtime

    > In Colaboratory, click the "Connect" button and select "Connect to local runtime...". Enter the URL from the previous step in the dialog that appears and click the "Connect" button. After this, you should now be connected to your local runtime.
