const express = require("express");
const { json } = require("body-parser");
const mongoose = require("mongoose");
const curso_router = require("../routes/curso");
const usuario_router = require("../routes/usuario");
const comentario_router = require("../routes/comentario");
const imagen_router = require("../routes/imagen");
require("dotenv").config();

module.exports = class Server {
  constructor() {
    this.app = express();
    this.puerto = process.env.PORT || 5000;
    this.CORS();
    this.bodyParser();
    this.rutas();
    this.conectarMongoDb();
  }
  CORS() {
    this.app.use((req, res, next) => {
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Header", "Content-Type, Authorization");
      res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
      next();
    });
  }
  bodyParser() {
    this.app.use(json());
  }
  rutas() {
    this.app.get("/", (req, res) => {
      return res
        .json({
          success: true,
          content: null,
          message: "Bienvenido a mi API",
        })
        .end();
    });
    this.app.use(curso_router, usuario_router, imagen_router);
  }
  async conectarMongoDb() {
    // "mongodb://localhost:27017/plataforma_educativa"
    await mongoose
      .connect(process.env.MONGO_COMPASS, {
        useNewUrlParser: true, // para indicar que estamos usando el nuevo formato de coneccion url
        useUnifiedTopology: true, // para indicar que vamos a usar un nuevo motor de administracion de conecciones,
        // solamente indicar false cuando la conexion sea poco estable
        useCreateIndex: true,
        useFindAndModify: false,
      })
      .catch((e) => console.errors(e));
    console.log("Base de datos conectada exitosamente");
  }

  start() {
    this.app.listen(this.puerto, () => {
      console.log(`Servidor corriendo en http://127.0.0.1:${this.puerto}`);
    });
  }
};
