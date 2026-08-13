import time
import json
import re
import requests
import os

from config import DOWNLOAD_FOLDER, FINAL_FILE, PPA_TARGET


CHANGELOG_REGEX = r"\((.*)\)"


def untar_package(archive: str, package_path: str) -> None:
    os.makedirs(package_path)
    os.system(f"tar -xvf {archive} -C {package_path} --strip-components=1")


def parse_packages_inside_archive(package_path: str) -> list[str] | None:
    # this is the only way I found to list all dependencies
    control_file_name = f"{package_path}/debian/control"

    with open(control_file_name, "r") as f:
        for line in f.read().splitlines():
            if line.startswith("Depends: "):
                line = line.replace("Depends: ", "")
                return line.split(", ")
    return None


def parse_version(package_path: str) -> str | None:
    changelog_file_name = f"{package_path}/debian/changelog"

    with open(changelog_file_name, "r") as f:
        content = f.read()
        matches = re.search(CHANGELOG_REGEX, content, re.MULTILINE)

        if not matches:
            return None

        return matches.groups()[0]
    return None


def create_last_updated_file() -> None:
    with open("last_updated_at.js", "w") as f:
        f.write("export default ")
        f.write(f'"{time.ctime()}"')


# Most documentation from https://api.launchpad.net/devel.html#archive
def get_package_release_codename(package_name: str, version: str) -> str | None:
    params = {
        "ws.op": "getPublishedSources",
        # Let's not get packages that are already superseded
        "status": "Published",
        "pocket": "Release",
        "source_name": package_name,
        "version": version,
        "order_by": "published_date_desc",
    }

    try:
        res = requests.get(
            f"https://api.launchpad.net/devel/~{PPA_TARGET['author']}/+archive/ubuntu/{PPA_TARGET['archive_name']}",
            params=params,
            timeout=10,
        )

        if not res.ok:
            return None

        res = res.json()

        if res["total_size"] < 1:
            return None

        return res["entries"][0]["display_name"].split(" in ")[1]
    except Exception as e:
        print(f"An error occured: {e}")
        return None


def main():
    result = []

    for archive in sorted(os.listdir(DOWNLOAD_FOLDER)):
        package_name = archive.replace(".tar.xz", "")
        archive = f"{DOWNLOAD_FOLDER}/{archive}"
        package_path = archive.replace(".tar.xz", "")

        untar_package(archive, package_path)
        packages = parse_packages_inside_archive(package_path)
        if packages is None:
            print(f"Couldn't find sub-packages for {package_name}")
            continue

        version = parse_version(package_path)

        release = get_package_release_codename(package_name, version)

        result.append(
            {
                "name": package_name,
                "packages": sorted(packages),
                "version": version,
                "release": release,
            }
        )

    with open(FINAL_FILE, "w") as f:
        f.write("export default ")
        f.write(json.dumps(result))

    create_last_updated_file()


if __name__ == "__main__":
    main()
