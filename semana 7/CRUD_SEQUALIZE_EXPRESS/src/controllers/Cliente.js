const { Cliente } = require("../config/Creacion");

const crearCliente = async (req, res) => {
  // solamente un usuario logueado puede crear clientes
  const nuevoCliente = await Cliente.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear Cliente",
    })
  );
  return res.status(201).json({
    success: true,
    content: nuevoCliente,
    message: "Cliente creado exitosamente",
  });
};

const devolverClientes = async (req, res) => {
  const clientes = await Cliente.findAll().catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al obtener clientes",
    })
  );
  return res.json({
    success: true,
    content: clientes,
    message: null,
  });
};

module.exports = { crearCliente, devolverClientes };
