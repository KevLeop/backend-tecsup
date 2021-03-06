const { Router } = require("express");
const usuario_controller = require("../controllers/usuario");
const { wachiman } = require("../utils/validador");
const Multer = require("multer");

const usuario_router = Router();

const multer = Multer({
  storage: Multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024,
  },
});

usuario_router.post("/registro", usuario_controller.registro);
usuario_router.post("/login", usuario_controller.login);
usuario_router.post("/inscribir", wachiman, usuario_controller.inscribirCurso);
usuario_router.get(
  "/mostrarcursos",
  wachiman,
  usuario_controller.mostrarCursosUsuario
);

usuario_router.put(
  "/actualizarUsuario",
  wachiman,
  multer.single("imagen"),
  usuario_controller.editarUsuario
);

usuario_router.post(
  "/cambiar-password",
  wachiman,
  usuario_controller.cambiarPassword
);

usuario_router.post("/reset-password", usuario_controller.resetPassword);
usuario_router.get("/validar-hash", usuario_controller.consultarHash);
usuario_router.post("/new-password", usuario_controller.changePassword);

module.exports = usuario_router;
