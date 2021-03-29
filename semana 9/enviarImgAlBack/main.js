const nombre = document.getElementById("inputNombre");
const cantidad = document.getElementById("inputCantidad");
const precio = document.getElementById("inputPrecio");
const foto = document.getElementById("inputFoto");
const registrar = document.getElementById("btnRegistrar");
const mostrar = document.getElementById("btnMostrar");
const informacion = document.getElementById("platos");

const BASE_URL = "http://127.0.0.1:8000";

const formData = new FormData();
registrar.addEventListener("click", async (e) => {
  e.preventDefault();
  formData.append("platoDescripcion", nombre.value);
  formData.append("platoCantidad", cantidad.value);
  formData.append("platoPrecio", precio.value);
  formData.append("platoFoto", foto.files[0]);
  console.log(nombre.value);
  console.log(foto.files[0]);
  const resultado = await fetch(BASE_URL + "/plato", {
    method: "POST",
    body: formData,
    // headers: {
    //   Authorization : "Beareer 123123.123123.123123"
    // }
  });
  const json = await resultado.json();
  console.log(json);
});

mostrar.addEventListener("click", async (e) => {
  e.preventDefault();
  const resultado = await fetch(BASE_URL + "/plato", {
    method: "GET",
  });
  const json = await resultado.json();
  informacion.innerText = JSON.stringify(json);
});
