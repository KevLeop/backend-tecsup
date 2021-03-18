const { Promocion } = require("../config/Creacion");

const crearPromocion = async (req, res) => {
  const nuevaPromocion = await Promocion.create(req.body).catch((error) =>
    res.status(500).json({
      success: false,
      content: error,
      message: "Error al crear la promo",
    })
  );
  return res.status(201).json({
    success: true,
    content: nuevaPromocion,
    message: "Promocion creada exitosamente",
  });
};

const devolverPromociones = async (req, res) => {
  const promociones = await Promocion.findAll();
  return res.json({
    success: true,
    content: promociones,
    message: null,
  });
};

module.exports = {
  crearPromocion,
  devolverPromociones,
};
