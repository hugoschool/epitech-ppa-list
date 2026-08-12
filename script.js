import packages from "./packages/packages.js";
import last_updated_at from "./last_updated_at.js";
const root = document.getElementById("root");

console.log(packages);
packages.forEach(element => {
    const div = document.createElement("div");

    const name = document.createElement("h1");
    name.innerText = element["name"];
    name.id = element["name"];

    const details = document.createElement("p");

    const version = document.createElement("span");
    version.style = "font-weight: bold;";
    version.innerText = `Version: ${element["version"]}`;

    const release = document.createElement("span");
    release.innerText = `Release: ${element["release"]}`;

    details.append(version);
    details.append(document.createElement("br"));
    details.append(release);

    const packages_list = document.createElement("ul");
    element["packages"].forEach(dep => {
        const single_package = document.createElement("li");
        single_package.innerText = dep;
        packages_list.append(single_package);
    });

    div.append(name);
    div.append(details);
    div.append(packages_list);
    root.append(div);
});

const last_updated_elem = document.getElementById("last_updated_at");
last_updated_elem.innerText = last_updated_at;
