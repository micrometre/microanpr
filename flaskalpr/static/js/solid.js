import { onCleanup, createSignal, createResource } from "https://esm.sh/solid-js@1.8.1";
import { render } from "https://esm.sh/solid-js@1.8.1/web";
import html from "https://esm.sh/solid-js@1.8.1/html";




const Plates = () => {
    const [plates, setPlates] = createSignal([])
    var source = new EventSource("http://34.105.172.98:5000/alprd1/alprd1   ");
    //var source = new EventSource("http://192.168.1.122:5000/alprd1/alprd1   ");
    //var source = new EventSource("http://192.168.1.197:5000/alprd1/alprd1");
    source.onmessage = function (event) {
        const alprdData = JSON.parse(event.data)
        setPlates(alprdData)
    };
    return html`
     <div class="position-relative overflow-hidden p-1 p-md-1 m-md-1 text-center">
        <h2 class="pt-2 mt-2 mb-2 display-4 fw-bold">
        ${plates}
       </h2>
    </div>
    `;
};
//render(Plates, document.body);
render(Plates, document.getElementById('alprd-plates'));





const PlatesImages = () => {
    const [PlatesImages, setPlatesImages] = createSignal([])
    function onError(e) {
        e.target.src =
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/No_sign.svg/192px-No_sign.svg.png";
    }

    var source = new EventSource("http://34.105.172.98:5000/alprd1_images");
    //var source = new EventSource("http://192.168.1.122:5000/alprd1_images");
    //var source = new EventSource("http://192.168.1.197:5000/alprd1_images/");
    source.onmessage = function (event) {
        const alprdData = event.data
        setPlatesImages(alprdData)
        console.log(alprdData)
        const img = document.getElementById("alpr-image")
        img.addEventListener("error", function (event) {
            event.target.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/No_sign.svg/192px-No_sign.svg.png";

            event.onerror = null
        })


    };
    return html`
        <div class="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center">
        <img src=${PlatesImages} class="img-thumbnail" id="alpr-image" alt="...">
        <a target="_blank" href=${PlatesImages}>
        <div  id="alpr-image-div" >${PlatesImages}</div>
        </a>

            </a>
        </div>
    
        `;
};
render(PlatesImages, document.getElementById('alprd-images'));