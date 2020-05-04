#!/usr/bin/env bash

# Variables
readonly projectDir=$(realpath "$(dirname ${BASH_SOURCE[0]})/..")

####################################################################################################
# Set bazel configuration for CircleCI runs.
####################################################################################################
cp "${projectDir}/.circleci/.bazelrc" "$HOME/.bazelrc";
