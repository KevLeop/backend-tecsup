const { Router } = require("express");
const categoria_controller = require("../controllers/Categoria");

const categoria_router = Router();
categoria_router.post("/categoria", categoria_controller.crearCategoria);
categoria_router.get("/categoria", categoria_controller.devolverCategorias);
categoria_router.get(
  "/categoria/:id",
  categoria_controller.devolverCategoriaPorId
);
categoria_router.put(
  "/categoria/:id",
  categoria_controller.editarCategoriaPorId
);

categoria_router.delete(
  "/categoria/:id",
  categoria_controller.eliminarCategoriaPorId
);

categoria_router.get(
  "/buscarCategoria",
  categoria_controller.listarCategoriasLikeName
);

module.exports = categoria_router;
