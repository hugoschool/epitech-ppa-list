import packages from "./packages/packages.js";
import last_updated_at from "./last_updated_at.js";
const root = document.getElementById("root");

console.log(packages);
packages.forEach(element => {
    const div = document.createElement("div");

    const name = document.createElement("h1");
    name.innerText = element["name"];
    name.id = element["name"];

    const version = document.createElement("h4");
    version.innerText = `Version: ${element["version"]}`;

    const packages_list = document.createElement("ul");
    element["packages"].forEach(dep => {
        const single_package = document.createElement("li");
        single_package.innerText = dep;
        packages_list.append(single_package);
    });

    div.append(name);
    div.append(version);
    div.append(packages_list);
    root.append(div);
});

const last_updated_elem = document.getElementById("last_updated_at");
last_updated_elem.innerText = last_updated_at;
