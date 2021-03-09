const express = require("express");
const { json } = require("body-parser");
const { conexion } = require("./Sequelize");

module.exports = class Server {
  constructor() {
    this.app = express();
    this.puerto = process.env.PORT || 5000;

    this.CORS();
    this.configurarBodyParser();
    this.rutas();
  }
  CORS() {
    // Los CORS son el control de acceso a nuestra API, definimos que dominios pueden acceder,
    // qué metodos se pueden acceder y qué headers se pueden enviar
    this.app.use((req, res, next) => {
      // Access-Control-Allow-Origin => indica que dominio(s) pueden acceder a mi API
      res.header("Access-Control-Allow-Origin", "*");
      // Access-Control-Allow-Headers => para indicar qué tipos de cabeceras me puede mandar el front
      res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
      // Access-Control-Allow-Methods => para indicar qué metodos pueden acceder a mi API
      res.header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE");
      next();
    });
  }
  configurarBodyParser() {
    this.app.use(json());
  }
  rutas() {
    this.app.get("/", (req, res) => {
      res.json({
        message: "Bienvenido a mi API",
      });
    });
  }
  start() {
    this.app.listen(this.puerto, async () => {
      console.log(`Servidor corriendo con exito en el puerto: ${this.puerto}`);
      try {
        let respuesta = await conexion.sync();
        console.log(respuesta.config);
        console.log("Base de datos sincronizada correctamente");
      } catch (error) {
        console.log(error);
      }
    });
  }
};
