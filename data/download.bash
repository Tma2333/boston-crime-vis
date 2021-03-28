#!/usr/bin/env bash
mkdir -p ~/.kaggle
cp ./kaggle.json ~/.kaggle/
sudo chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download --unzip -d ankkur13/boston-crime-data