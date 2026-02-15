#!/bin/env bash

# This script is used to first install the dependencies and configure the environment

pkg update -y
pkg install -y python cronie termux-services
pip install requests beautifulsoup4 python-dotenv

target_dir="$HOME/fr.what"
[[ -d "$target_dir" ]] && rm -rf "$target_dir"

git clone https://github.com/gabe-frasz/fr.what.git "$target_dir"
