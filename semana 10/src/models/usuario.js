const { Schema } = require("mongoose");
const { imagenSchema } = require("./imagen");
const { hashSync } = require("bcrypt");

const telefonoSchema = new Schema({
  fono_codigo: {
    type: Number,
    min: 1,
    max: 99,
  },
  fono_numero: {
    type: String,
    minlegth: 6,
    maxlength: 10,
  },
});

const usuarioSchema = new Schema(
  {
    usuario_nombre: {
      type: String,
      required: true,
      alias: "usu_nomb",
    },
    usuario_apellido: {
      type: String,
      maxlength: 25,
    },
    usuario_email: {
      type: String,
      maxlength: 50,
      minlength: 25,
      unique: true,
    },
    usuario_password: String,
    usuario_categoria: {
      type: Number,
      min: 1,
      max: 4,
    },
    usuario_telefono: [telefonoSchema],
    usuario_imagen: imagenSchema,
    cursos: [Schema.Types.ObjectId],
    comentarios: [Schema.Types.ObjectId],
  },
  {
    timestamps: {
      createdAt: "fecha_creacion",
      updatedAt: "fecha_actualizacion",
    },
  }
);

usuarioSchema.methods.encriptarPassword = async function (password) {
  this.usuario_password = hashSync(password, 10);
};
module.exports = {
  usuarioSchema,
};
