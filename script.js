import packages from "./packages/packages.js";
const root = document.getElementById("root");

console.log(packages);
packages.forEach(element => {
    const div = document.createElement("div");

    const name = document.createElement("h1");
    name.innerText = element["name"];

    const packages_list = document.createElement("ul");
    element["packages"].forEach(dep => {
        const single_package = document.createElement("li");
        single_package.innerText = dep;
        packages_list.append(single_package);
    });

    div.append(name);
    div.append(packages_list);
    root.append(div);
});
