const { Usuario } = require("../config/mongoose");

const registro = async (req, res) => {
  const objUsuario = new Usuario(req.body);
  objUsuario.encriptarPassword(req.body.password);
  const usuarioCreado = await objUsuario.save().catch((error) => {
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear el usuario",
    });
  });
  return res.status(201).json({
    success: true,
    content: usuarioCreado,
    message: "Usuario creado exitosamente",
  });
};

const login = async (req, res) => {
  const { email, password } = req.body;
  const usuarioEncontrado = await Usuario.findOne({
    usuario_email: email,
  }).catch((error) => {
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al buscar usuario",
    });
  });
  if (!usuarioEncontrado) {
    return res.status(404).json({
      success: false,
      content: null,
      message: "Correo no se encuentra",
    });
  }

  if (usuarioEncontrado.validarPassword(password)) {
    return res.status(201).json({
      success: true,
      content: usuarioEncontrado.generarJWT(),
      message: "Usuario logueado exitosamente",
    });
  } else {
    res.status(500).json({
      success: false,
      content: error,
      message: "Constraseña incorrecta",
    });
  }
};

module.exports = {
  registro,
  login,
};
