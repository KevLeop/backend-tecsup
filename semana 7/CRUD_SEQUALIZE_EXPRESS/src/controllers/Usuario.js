const { Usuario } = require("../config/Creacion");

const registro = async (req, res) => {
  // creacion en dos 02 pasos
  // 1. construimos el objeto usuario
  const { password } = req.body;
  const nuevoUsuario = Usuario.build(req.body);
  nuevoUsuario.setearPassword(password);
  // 2. Una vez realizadas las modificaciones a nuestro objeto, los guardamos en la BD
  await nuevoUsuario.save();
  return res.status(201).json({
    success: true,
    content: nuevoUsuario,
    message: "Usuario creado exitosamente",
  });
};

const login = async (req, res) => {
  const { email, password } = req.body;
  // 1. validar si el correo existe
  const usuario = await Usuario.findOne({ where: { usuarioEmail: email } });
  if (usuario) {
    // 2. validar si la contraseña existe
    const resultado = usuario.validarPassword(password);
    console.log(resultado);
    if (resultado) {
      const token = usuario.generarJWT();
      // devolvemos la token
      return res.json({
        success: true,
        content: token,
        message: "Bievenido!!",
      });
    } else {
      return res.status(404).json({
        success: false,
        content: null,
        message: "Usuario o contraseña incorrectos",
      });
    }
  } else {
    return res.status(404).json({
      success: false,
      content: null,
      message: "Usuario o contraseña incorrectos",
    });
  }
};

module.exports = { registro, login };
