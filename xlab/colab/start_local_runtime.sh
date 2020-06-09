# https://research.google.com/colaboratory/local-runtimes.html
bazel run //xlab/colab:start_local_runtime -- \
  --NotebookApp.allow_origin='https://colab.research.google.com' \
  --port=8888 \
  --NotebookApp.port_retries=0 \
  # This shouldn't be necesary: https://github.com/dillon-giacoppo/rules_python_external/issues/18
  --config=$(pwd)/.venv/etc/jupyter/jupyter_notebook_config.json
