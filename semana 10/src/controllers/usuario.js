const { Usuario } = require("../config/mongoose");
const { Curso } = require("../config/mongoose");

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

const inscribirCurso = async (req, res) => {
  /**
   * 1. usar la token para ver que usuario esta queriendo acceder a que curso
   * 2. mediante la url indicar el id del curso (query)
   * 2.1 ver si el curso existe
   * 3. ver si el usuario ya esta inscrito en el curso y si lo esta no permitir volver a inscribirlo
   * 4. si no esta inscrito, inscribirlo
   */

  const { id } = req.query;
  const { usuario_id } = req.usuario;
  const cursoEncontrado = await Curso.findById(id).catch((error) => {
    res.status(404).json({
      success: false,
      content: error,
      message: "No se encontro el curso",
    });
  });

  if (cursoEncontrado) {
    const { cursos } = await Usuario.findById(usuario_id);
    for (const key in cursos) {
      if (cursos[key] === id) {
        return res.json({
          success: false,
          content: null,
          message: "Usuario ya se encuentra registrado en el curso",
        });
      }
    }
    console.log(req.usuario);
    res.send("ok");
    console.log(cursoEncontrado);
  }
};

module.exports = {
  registro,
  login,
  inscribirCurso,
};
