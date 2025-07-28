#!/bin/sh
# Update all project documentation submodules to the latest commits.

set -e

git submodule update --remote --recursive "$@"
