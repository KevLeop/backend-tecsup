let temarios = [];

const crearTemario = (req, res) => {
  // request: para recibir todo lo que el usuario nos esté mandando
  console.log(req.body);
  temarios.push(req.body);
  return res.json({
    success: true,
    content: req.body,
    message: "Tema creado exitosamente",
  });
};

const devolverTemarios = (req, res) => {
  return res.json({
    success: true,
    content: temarios,
    message: null,
  });
};

const editarTemario = (req, res) => {
  console.log(req.params);
  let { id } = req.params;
  console.log(temarios[id]);
  if (temarios[id]) {
    console.log("hay temarios");
    temarios[id] = req.body;
    return res.json({
      succes: true,
      content: temarios[id],
      message: "Temario actualizado ocn exito",
    });
  } else {
    console.log("no hay temarios");
    return res.status(404).json({
      success: false,
      content: null,
      message: "Temario no exist",
    });
  }
};

const eliminarTemario = (req, res) => {
  let { id } = req.params;
  if (temarios[id]) {
    let eliminado = temarios.splice(id, 1);
    console.log(temarios);
    return res.json({
      succes: true,
      content: eliminado,
      message: "Temario eliminado ocn exito",
    });
  } else {
    return res.status(404).json({
      success: false,
      content: null,
      message: "Temario no exist",
    });
  }
};

module.exports = {
  crearTemario,
  devolverTemarios,
  editarTemario,
  eliminarTemario,
};
