#!/bin/bash

set -o errexit

git submodule update --init --recursive
ansible-galaxy install -r roles/requirements.yml
ansible-galaxy collection install -r collections/requirements.yml
