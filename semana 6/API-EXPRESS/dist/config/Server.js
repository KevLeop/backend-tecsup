// npm install express

const express = require("express");
const temario_router = require("../routes/Temario");
const bodyParser = require("body-parser");

class Server {
  constructor() {
    this.app = express();
    this.puerto = process.env.PORT || 5000;
    this.configurarBodyParser();
    this.rutas();
  }

  configurarBodyParser() {
    this.app.use(bodyParser.json());
  }

  rutas() {
    this.app.get("/", (req, res) => {
      // el request es todo lo que manda el cliente
      // response: la dorma en la cual responde
      console.log("El cliente me llama!");
      return res.status(200).send("Bienvenido a mi api");
    });

    this.app.use("/api", temario_router);
  }

  iniciarServidor() {
    this.app.listen(this.puerto, () => {
      console.log(
        `El servidor se ha levantado exitosamente en el puerto ${this.puerto}`
      );
    }); // se queda escuchando al servidor que se levantara mediante un determinado puerto
  }
}

module.exports = Server;
