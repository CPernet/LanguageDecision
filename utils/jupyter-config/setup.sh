#!/bin/bash
# This will only work on Linux/MacOS hosts!

script_dir="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
config_dir=$(jupyter --config-dir)

# Add post-save hook to jupyter notebook configuration
cat $script_dir/post-save-hook.py >> $config_dir/jupyter_notebook_config.py
