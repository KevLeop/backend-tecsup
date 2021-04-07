const { Usuario } = require("../config/mongoose");
const { Curso } = require("../config/mongoose");
const { subirArchivo } = require("../utils/manejadorFirebaseStorage");

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

  const curso_id = req.query.id;
  const { usuario_id } = req.usuario;

  const cursoEncontrado = await Curso.findById(curso_id).catch((error) => {
    console.log(error);
    res.status(404).json({
      success: false,
      content: error,
      message: "No se encontro el curso",
    });
  });
  console.log(cursoEncontrado);
  if (cursoEncontrado) {
    const usuarioEncontrado = await Usuario.findById(usuario_id);
    const resultado = usuarioEncontrado.cursos.includes(curso_id);
    const resultadoCurso = cursoEncontrado.usuarios.includes(usuario_id);

    if (resultado && resultadoCurso) {
      return res.status(401).json({
        success: false,
        content: null,
        message: "Usuario ya se encuentra registrado en el curso",
      });
    }
    usuarioEncontrado.cursos.push(curso_id);
    usuarioEncontrado.save();

    cursoEncontrado.usuarios.push(usuario_id);
    cursoEncontrado.save();

    return res.status(201).json({
      success: true,
      content: usuarioEncontrado,
      message: "Usuario enrolado exitosamente",
    });
  } else {
    return res.status(404).json({
      success: false,
      content: null,
      message: "No se encontro el curso",
    });
  }
};

// mostrar los cursos del usuario
const mostrarCursosUsuario = async (req, res) => {
  const { usuario_id } = req.usuario;
  const { cursos } = await Usuario.findById(usuario_id);
  console.log(cursos);
  let resultado;
  resultado = await Promise.all(
    cursos.map((curso) =>
      Curso.findById(
        curso,
        "curso_nombre curso_descripcion curso_link curso_imagenes"
      )
    )
  );
  return res.json({
    success: true,
    content: resultado,
    message: "ok",
  });
};

const editarUsuario = async (req, res) => {
  const { usuario_id } = req.usuario;
  const link = await subirArchivo(req.file).catch((error) =>
    res.json({
      success: false,
      content: error,
      message: "Error al subir la imagen",
    })
  );
  if (link) {
    req.body.usuario_imagen = { imagen_url: link };
    const usuarioActualizado = await Usuario.findByIdAndUpdate(
      usuario_id,
      req.body,
      { new: true }
    );
    return res.json({
      success: true,
      content: usuarioActualizado,
      message: null,
    });
  }
};

module.exports = {
  registro,
  login,
  inscribirCurso,
  mostrarCursosUsuario,
  editarUsuario,
};
