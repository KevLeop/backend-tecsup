const { verify } = require("jsonwebtoken");
const password = process.env.JWT_SECRET || "password";
const { Usuario } = require("../config/Creacion");

const verificarToken = (token) => {
  try {
    // sirve para verificar la autenticidad, validez y que esté correctamente formateada
    // la token, si lo está devolvera el payload caso contrario,  saltará el catch
    const payload = verify(token, password, { algorithm: "RS256" });
    return payload;
  } catch (error) {
    // si la token no es valida, la password no concuerda o si ya expiro saltará el catch
    // y nos devolverá un json con la llave message en la cual se mostrará el mensaje que suscitó el error
    // name => nombre del error
    // expiredAt => fecha en la que expiró la token
    return error.message;
  }
};

const wachiman = (req, res, next) => {
  // primero validamos si me está dando un token
  if (req.headers.authorization) {
    // dentro de mis heades¿rs voy a buscar la llave authorization
    // ahora tengo que utilizar la token que me este dando
    // Bearer 1231321.23113215.asdas654
    const token = req.headers.authorization.split(" ")[1];
    const respuesta = verificarToken(token);
    // si el tipo de dato de la rpta es un objeto(payload) (token verifiada) caso contrario
    // si es un string (error)
    if (typeof respuesta === "object") {
      next();
    } else {
      return res.status(401).json({
        success: false,
        content: respuesta,
        message: "No estas autorizado para realizar esta solicitud",
      });
    }
  } else {
    return res.status(404).json({
      success: false,
      content: null,
      message: "Se requiere autorizacion para realizar esta peticion",
    });
  }
};

module.exports = {
  wachiman,
};
