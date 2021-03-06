const { Router } = require("express");
// const { crearTemario, devolverTemarios } = require("../controllers/Temario");
const temarioController = require("../controllers/Temario");
const temario_router = Router();

temario_router.post("/temario", temarioController.crearTemario);
temario_router.get("/temario", temarioController.devolverTemarios);
temario_router.put("/temario/:id", temarioController.editarTemario);
temario_router.delete("/temario/:id", temarioController.eliminarTemario);
module.exports = temario_router;
