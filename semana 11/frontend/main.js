const socket = io("http://127.0.0.1:3000");
const nombre = document.getElementById("nombre");
const ingresar = document.getElementById("ingresar");
const listaUsuarios = document.getElementById("lista-usuarios");
const mensaje = document.getElementById("mensaje");
const listaMensajes = document.getElementById("lista-mensajes");

// connect: sirve para conectarnos al socket (y el backend recibira la notificaion de la nueva conexion)
// el metodo on sirve para mandar algo al back
socket.on("connect", () => {
  console.log("conectado");
});

// el metodo emit sirve para enviar algo al back mediente el nombre de su socket

ingresar.addEventListener("click", (e) => {
  e.preventDefault();
  const classbtn = ingresar.classList;
  if (classbtn.contains("btn-danger")) {
    socket.disconnect().connect();
    // ^^ sirve para hacer un hard-reset del client del socket (expulsa al cliente)
    // y automaticamente se intenta reconectar
    ingresar.innerText = "Ingresar al chat";
    ingresar.className = "btn btn-block btn-success";
    nombre.disabled = false;
    nombre.value = "";
  } else {
    socket.emit("configurar-cliente", nombre.value);
    // ingresar.disabled = true;
    nombre.disabled = true;
    ingresar.className = "btn btn-danger btn-block";
    ingresar.innerText = "Salir del chat";
  }
});

socket.on("lista-usuarios", (usuarios) => {
  console.log(usuarios);
  listaUsuarios.innerHTML = "";
  for (const key in usuarios) {
    const usuarioLi = document.createElement("li");
    usuarioLi.className = "list-group-item";
    usuarioLi.innerText = usuarios[key].nombre;
    listaUsuarios.appendChild(usuarioLi);
  }
});

mensaje.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    socket.emit("mensaje", mensaje.value);
    mensaje.value = "";
  }
});

socket.on("lista-mensajes", (mensajes) => {
  console.log(mensajes);

  listaMensajes.innerHTML = "";
  mensajes.forEach((mensaje) => {
    const mensajeLi = document.createElement("li");
    mensajeLi.className = "list-group-item";
    mensajeLi.innerText = `${mensaje.cliente} dice: ${mensaje.mensaje}`;
    listaMensajes.appendChild(mensajeLi);
  });
});
