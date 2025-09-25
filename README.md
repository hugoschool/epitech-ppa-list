# Epitech PPA List

List of all dependencies inside [Epitech's PPA](https://launchpad.net/~epitech/+archive/ubuntu/ppa) packages used for the official [Ubuntu dump](https://github.com/Epitech/dump).

It used to be very easy to see all dependencies installed and used by the [official docker image](https://github.com/Epitech/epitest-docker) until the usage of the Ubuntu PPA which makes it harder to see.

This is useful for people not running the Ubuntu dump and using a different distro.

## Usage

```sh
python3 scripts/fetch_all_packages.py
python3 scripts/extract_packages.py
```
