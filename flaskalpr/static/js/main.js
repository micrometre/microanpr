
let file = "http://192.168.1.197/upload_images/uploaddb"
fetch(file)
    .then(x => x.text())
    .then(y => document.getElementById("uploaddb").innerHTML = y);

let file2 = "http://192.168.1.197/upload_images/uploaddb"
fetch(file)
    .then(console.log(file))