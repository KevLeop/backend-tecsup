const { Curso } = require("../config/mongoose");

const crearCurso = async (req, res) => {
  console.log("ingerso al controller");
  try {
    const nuevoCurso = new Curso(req.body);
    // aqui ira la ogica de subida de imagenes
    const cursoCreado = await nuevoCurso.save();
    return res.status(201).json({
      success: true,
      content: cursoCreado,
      message: "Curso creado exitosamente",
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear el curso",
    });
  }
};

module.exports = {
  crearCurso,
};
