#!/usr/bin/env bash

set -euo pipefail

PACKAGES_PATH="packages/archives"

if ! [ -d "$PACKAGES_PATH" ]; then
    echo "Impossible to find the archived packages path."
    exit 1
fi

read -p "WARNING: this script will delete all decompressed packages in '$PACKAGES_PATH', are you sure to proceed? (y/n) " yn
case $yn in
    [Yy]* )
        find "$PACKAGES_PATH" -not -path "$PACKAGES_PATH" -type d -exec rm -rf {} \+
        ;;
    [Nn]* )
        exit
        ;;
    * )
        exit
        ;;
esac
