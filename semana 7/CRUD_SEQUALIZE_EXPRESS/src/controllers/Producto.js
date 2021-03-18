const { Producto, Categoria } = require("../config/Creacion");
// const Producto = require("../models/Producto")();
const { Op } = require("sequelize");

const crearProducto = async (req, res) => {
  const nuevoProducto = await Producto.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear producto",
    })
  );
  return res.status(201).json({
    success: true,
    content: nuevoProducto,
    message: "Producto creado exitosamente",
  });
};

// hacer el devoler producto por busqueda por nombre
const devolverProductosPorNombre = async (req, res) => {
  let { nombre } = req.query;
  console.log(nombre);
  let filtro = await Producto.findAll({
    where: {
      productoEstado: true,
      productoNombre: {
        [Op.like]: "%" + nombre + "%",
      },
    },
    include: {
      model: Categoria,
    },
  }).catch((error) => {
    return res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error filtrar producto",
    });
  });
  console.log(filtro);
  return res.json({
    success: true,
    content: filtro,
    message: "Consulta exitosa",
  });
};

const editarProducto = async (req, res) => {
  let { id } = req.params;
  console.log(id);
  const resultado = await Producto.update(req.body, {
    where: {
      productoId: id,
    },
  }).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Hubo un error al editar producto",
    })
  );
  return res.status(201).json({
    success: true,
    content: resultado,
    message: null,
    // resultado[0] === 0 ? "No se actualizo nada" : "Se actualizo exitosamente",
  });
};

module.exports = {
  crearProducto,
  devolverProductosPorNombre,
  editarProducto,
};
