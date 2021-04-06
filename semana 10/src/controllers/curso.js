const { Curso } = require("../config/mongoose");
const { cursoSchema } = require("../models/curso");

const crearCurso = async (req, res) => {
  console.log("ingerso al controller");
  try {
    const nuevoCurso = new Curso(req.body);
    // aqui ira la logica de subida de imagenes

    // Forma 2: en un solo paso
    //cursoCreado2 = await Curso.create(req.body)
    // Forma 3: Insertar varios recursos
    // Curso.insertMany(req.body)
    //    req.body => Array de objetos curso

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

const listarCursos = async (req, res) => {
  const cursos = await Curso.find().catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "error al devolver cursos",
    })
  );
  return res.json({
    success: true,
    content: cursos,
    message: null,
  });
};

const listarCursosPorNombre = async (req, res) => {
  const { nombre } = req.query;
  // * Primer Forma
  // https://mongoosejs.com/docs/api/query.html#query_Query-equals
  // const resultado = await Curso.find({
  //   curso_nombre: { $regex: ".*" + nombre + "*." },
  // });
  // * Segunda forma
  // const resultado= await Curso.where({
  //   curso_nombre: {$regex: '.*'+nombre+'*.'}
  // })

  // * Tercera forma
  const resultado = await Curso.where("curso_nombre")
    .equals({ $regex: ".*" + nombre + "*." })
    .where("curso_publicado")
    .equals(false);
  return res.json({
    success: true,
    content: resultado,
    message: null,
  });
};

const actualizarCurso = async (req, res) => {
  const { id } = req.params;
  // const resultado = await Curso.findOneAndUpdate({_id:id},req.body,{new:true}),  //new sirve para decidir si mostrar el registro actualizado(True) o el anterior(False)
  const resultado = await Curso.updateOne({ _id: id }, req.body).catch(
    (error) =>
      res.status(500).json({
        success: false,
        content: error,
        message: "Error al actualiza curso",
      })
  );
  return res.status(201).json({
    success: true,
    content: resultado,
    message: "Curso actualizado con exito",
  });
};

const eliminarCurso = async (req, res) => {
  const { id } = req.params;
  const resultado = await Curso.findOneAndDelete({ _id: id }).catch((error) => {
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al eliminar curso",
    });
  });
  return res.status(201).json({
    success: true,
    content: resultado,
    message: "Curso eliminado con exito",
  });
};

module.exports = {
  crearCurso,
  listarCursos,
  listarCursosPorNombre,
  actualizarCurso,
  eliminarCurso,
};
