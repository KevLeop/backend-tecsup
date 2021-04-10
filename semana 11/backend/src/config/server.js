import express from "express";
import { Server } from "http";
import socketIo from "socket.io";

export default class ServidorSocket {
  constructor() {
    this.app = express();
    this.puerto = process.env.PORT || 3000;
    this.httpServer = new Server(this.app);
    this.io = socketIo(this.httpServer, {
      //https://socket.io/docs/v4/handling-cors/
      cors: {
        origin: "*",
        // methods: ["GET", "POST"],  // Socket no maneja metodos, solo envia y recibe
      },
    });
    this.escucharSocket();
    this.rutas();
  }

  escucharSocket() {
    let usuarios = [];
    const mensajes = [];
    this.io.on("connect", (cliente) => {
      // console.log(cliente);
      this.io.emit("lista-usuarios", usuarios);
      console.log(`Se conecto el cliente ${cliente.id}`);
      cliente.on("disconnect", (motivo) => {
        console.log(`Se desconecto el cliente ${cliente.id}`);
        console.log(motivo);
        usuarios = usuarios.filter((usuario) => usuario.id !== cliente.id);
        // cuando hemos retirado al usuario del array, emitimos a todos la lista de usuarios
        this.io.emit("lista-usuarios", usuarios);
      });

      cliente.on("configurar-cliente", (nombre) => {
        usuarios.push({
          id: cliente.id,
          nombre,
        });
        this.io.emit("lista-usuarios", usuarios);
        // cliente.broadcast.emit("lista-usuarios", usuarios);
      });
      cliente.on("mensaje", (mensaje) => {
        const usuario = usuarios.filter(
          (usuario) => usuario.id === cliente.id
        )[0];
        console.log(usuario);
        mensajes.push({
          cliente: usuario.nombre,
          mensaje,
        });
        this.io.emit("lista-mensajes", mensajes);
      });
    });
  }

  rutas() {
    this.app.get("/", (req, res) => {
      res.json({
        success: true,
        content: null,
        message: "Bienvenido a mi app de sockets",
      });
    });
  }

  start() {
    this.httpServer.listen(this.puerto, () => {
      console.log(
        `Servidor corriendo exitosamente en : http://127.0.0.0:${this.puerto}`
      );
    });
  }
}
