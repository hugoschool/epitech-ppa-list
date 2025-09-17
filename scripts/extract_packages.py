import json
import os

from config import DOWNLOAD_FOLDER, FINAL_FILE


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

        result.append({"name": package_name, "packages": sorted(packages)})

    with open(FINAL_FILE, "w") as f:
        f.write(json.dumps(result))


if __name__ == "__main__":
    main()
