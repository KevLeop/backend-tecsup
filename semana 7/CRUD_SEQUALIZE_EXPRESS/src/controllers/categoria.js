const Categoria = require("../models/Categoria")();
const { Op } = require("sequelize");

// CREATE
crearCategoria = async (req, res) => {
  // si queremos resitrar los datos tal y como nos llega del fron usamos el metodo create,
  // si queremos modificar o validar primero usamos dos pasos que es .build()y luego el .save()

  const nuevaCategoria = await Categoria.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear la categoria",
    })
  );
  console.log(nuevaCategoria);
  return res.status(201).json({
    success: true,
    content: nuevaCategoria,
    message: "Categoria creada exitosamente",
  });
};

//READ ALL
const devolverCategorias = async (req, res) => {
  const categorias = await Categoria.findAll().catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al devolver las categorias",
    })
  );
  return res.json({
    success: true,
    content: categorias,
    message: null,
  });
};

// READ BY ID
const devolverCategoriaPorId = async (req, res) => {
  console.log(req.params);
  let { id } = req.params;
  const categoria = await Categoria.findByPk(id).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Ocurrió un error",
    })
  );
  return res.json({
    success: true,
    content: categoria,
    message: categoria ? null : "Categoria no existe",
  });
};

// UPDATE
const editarCategoriaPorId = async (req, res) => {
  let { id } = req.params;
  const resultado = await Categoria.update(req.body, {
    where: {
      categoriaId: id,
    },
  }).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al actualizar la categoria",
    })
  );
  console.log(resultado);
  return res.status(201).json({
    success: true,
    content: resultado,
    message:
      resultado[0] === 0 ? "No se actualizo nada" : "Se actualizo exitosamente",
  });
};

//DELETE
const eliminarCategoriaPorId = async (req, res) => {
  let { id } = req.params;
  const resultado = await Categoria.destroy({
    where: { categoriaId: id },
  }).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al eliminar categoria",
    })
  );
  return res.json({
    success: true,
    content: null,
    message:
      resultado !== 0
        ? "Categoria eliminada exitosamente"
        : "No se encontró la categoria",
  });
};

const listarCategoriasLikeName = async (req, res) => {
  console.log(req.query);
  let { nombre } = req.query;
  // SELECT * FROM T_CATEGORIA WHERE CAT_NOMBRE = NOMBRE
  const filtro = await Categoria.findAll({
    where: {
      categoriaNombre: {
        [Op.like]: "%" + nombre + "%",
      },
    },
  }).catch((error) => {
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error filtrar categoria",
    });
  });
  console.log(filtro);
  return res.json({
    success: filtro,
  });
};

module.exports = {
  crearCategoria,
  devolverCategorias,
  devolverCategoriaPorId,
  editarCategoriaPorId,
  eliminarCategoriaPorId,
  listarCategoriasLikeName,
};
