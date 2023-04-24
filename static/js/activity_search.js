function search_now(list) {
    const options = {
        threshold: 0.4,
        tokenize:true,
        keys: [
            "name",
            "category",
            "city",
            "state",
            "address"
        ]
    };

    let pattern = document.getElementById("search_box_change").value;

    const fuse = new Fuse(list, options);

    console.log(fuse.search(pattern));
    return fuse.search(pattern)
}