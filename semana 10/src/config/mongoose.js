const { model } = require("mongoose");
const { cursoSchema } = require("../models/curso");
const { usuarioSchema } = require("../models/usuario");
const comentarioSchema = require("../models/comentario");

const Usuario = model("usuario", usuarioSchema);
const Curso = model("curso", cursoSchema);
const Comentario = model("comentario", comentarioSchema);
module.exports = {
  Usuario,
  Curso,
  Comentario,
};
