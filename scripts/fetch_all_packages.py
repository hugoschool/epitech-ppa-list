import os
import re
import requests

from config import DOWNLOAD_FOLDER, PPA_CONFIG

HREF_REGEX = r"(?i)<a([^>]+)>(.+?)<\/a>"


def fetch_archive_name(url: str) -> str | None:
    res = requests.get(url, timeout=10)

    if not res.ok:
        return None

    # This allows to get only the inside of the <a> tag (which should be enough)
    matches = re.finditer(HREF_REGEX, res.text, re.MULTILINE)
    for match in matches:
        package_name = match.group(2)
        # only track tar.xz for extensions
        # (some older ppa don't use .tar.xz but .tar.gz)
        if package_name.endswith(".tar.xz"):
            return package_name

    return None


def download_archive(base_url: str, archive_name: str, final_path: str) -> None:
    res = requests.get(f"{base_url}/{archive_name}", timeout=10)

    os.makedirs(os.path.dirname(final_path), exist_ok=True)
    with open(final_path, "wb") as f:
        f.write(res.content)


def main():
    for ppa in PPA_CONFIG:
        base_link = f"https://ppa.launchpadcontent.net/{ppa['ppa']}/ubuntu/pool/main"

        for package in ppa["packages"]:
            package_link = f"{base_link}/{package[0]}/{package}"

            archive_name = fetch_archive_name(package_link)
            if archive_name is None:
                print(f"Couldn't find archive name for package {package}")
                continue

            final_path = f"{DOWNLOAD_FOLDER}/{archive_name}"

            download_archive(package_link, archive_name, final_path)

            new_final_path = final_path.replace(archive_name, f"{package}.tar.xz")
            os.rename(final_path, new_final_path)

            print(f"Downloaded {new_final_path}")


if __name__ == "__main__":
    main()
