const { verify } = require("jsonwebtoken");

const verificarToken = (token) => {
  try {
    const payload = verify(token, process.env.JWT_SECRET, {
      algorithm: "RS256",
    });
    return payload;
  } catch (error) {
    return error.message;
  }
};

const wachiman = (req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(400).json({
      success: false,
      content: null,
      message: "Necesitas estar autenticado para realizar esta funcion",
    });
  }
  const token = req.headers.authorization.split(" ")[1]; // [Bearer , 1qdas21sad.asdasd.asdasd]
  const respuesta = verificarToken(token);
  if (typeof respuesta === "object") {
    req.usuario = respuesta;
    next();
  } else {
    return res.status(401).json({
      success: false,
      content: respuesta,
      message: "No estas autorizado para realizar esta accion",
    });
  }
};

module.exports = {
  wachiman,
};
