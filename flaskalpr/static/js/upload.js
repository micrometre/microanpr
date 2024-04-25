function handleFileSelect(evt, input) {
  for (const file of evt.target.files) {
    const div = document.createElement('div')
    const src = URL.createObjectURL(file)
    div.innerHTML =
      `<img style="border: 1px solid #000; margin: 5px"  class="img-thumbnail"  ` +
      `src="${src}" title="${(file.name)}">`

    document.getElementById('list').insertBefore(div, null)
  }

}
document.getElementById('files').addEventListener('change', handleFileSelect, false);
document.getElementById("files").addEventListener("change", function () {
  if (this.files.length > 1) { // Limit to 5 files
    alert("You can only upload a maximum of 5 files.");
    this.value = ""; // Reset the input
  }
});


function update() {
  var element = document.getElementById("videoprogressBar");
  var width = 1;
  var identity = setInterval(scene, 10);
  function scene() {
    if (width >= 100) {
      clearInterval(identity);
    } else {
      width++;
      element.style.width = width + '%';
    }
  }
  document.location.reload(false)

}