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

  escucharSocket() {}

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
