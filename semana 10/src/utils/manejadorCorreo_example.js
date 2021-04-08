const nodeMailer = require("nodemailer");
const clienteCorreo = nodeMailer.createTransport({
  host: "smtp.gmail.com",
  port: 587,
  secure: false, // será true cuando el puerto sea el 465
  auth: {
    user: "", // correo fuente,
    pass: "", // contraseña de correo fuente,
  },
  tls: {
    rejectUnauthorized: false,
  },
});

const enviarCorreo = async (para, titulo, cuerpo) => {
  return new Promise((resolve, reject) => {
    clienteCorreo
      .sendMail({
        to: para,
        subject: titulo,
        text: cuerpo,
      })
      .then((resultado) => resolve(resultado))
      .catch((error) => reject(error));
  });
};

module.exports = { enviarCorreo };
