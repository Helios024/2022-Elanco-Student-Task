
async function data(){
    console.log("data")
    response = await fetch("http://127.0.0.1:8000/api/data/")
    window.location.reload();
}

async function resources(){
    console.log("resources")
    response = await fetch("http://127.0.0.1:8000/api/resources/")
    window.location.reload();
}
