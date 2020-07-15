# https://research.google.com/colaboratory/local-runtimes.html
# Note, the last line should not be necessary:
#   https://github.com/dillon-giacoppo/rules_python_external/issues/18
ibazel run //xlab/colab:start_local_runtime -- \
  --NotebookApp.allow_origin='https://colab.research.google.com' \
  --port=8888 \
  --NotebookApp.port_retries=0 \
  --config=$(pwd)/.venv/etc/jupyter/jupyter_notebook_config.json
