const root = document.getElementById("root");

fetch("packages/packages.json").then((response) => {
    return response.json();
}).then((res) => {
    console.log(res);
    res.forEach(element => {
        const div = document.createElement("div");

        const name = document.createElement("h1");
        name.innerText = element["name"];

        const packages_list = document.createElement("ul");
        element["packages"].forEach(package => {
            const single_package = document.createElement("li");
            single_package.innerText = package;
            packages_list.append(single_package);
        });

        div.append(name);
        div.append(packages_list);
        root.append(div);
    });
});
