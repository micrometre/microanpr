
//let file = "http://192.168.1.197:5000/upload_images/uploaddb"
//let file = "http://192.168.1.122:5000/upload_images/uploaddb"
let file = "http://34.105.172.98:5000/upload_images/uploaddb"
fetch(file)
    .then(x => x.text())
    .then(y => document.getElementById("uploaddb").innerHTML = y);

//let file2 = "http://192.168.1.197:5000/upload_images/uploaddb"
//let file2 = "http://192.168.1.122:5000/upload_images/uploaddb"
let file2 = "http://34.105.172.98:5000/upload_images/uploaddb"
fetch(file)
    .then(console.log(file))