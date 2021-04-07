const { Router } = require("express");
const Multer = require("multer");

const imagen_controller = require("../controllers/imagen");

const imagen_router = Router();

// configuramos multer
// * se le da atributos que guarden en la memory storage (en la RAM)+
const multer = Multer({
  storage: Multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024,
  },
});

imagen_router.post(
  "/subirImagen",
  multer.single("imagen"),
  imagen_controller.subirImagen
);

imagen_router.delete("/eliminarImagen", imagen_controller.eliminarImagen);

module.exports = imagen_router;
