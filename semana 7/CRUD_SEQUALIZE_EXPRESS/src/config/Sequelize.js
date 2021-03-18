const { Sequelize } = require("sequelize");

// 1. Forma de conectarse a la BD: uri
// const conexion = new Sequelize('mysql://usuario:password@host:puerto/base_datos',
// dialect:'mysql',
// timezone:'-05:00',
// dialectOptions: {
// // al momento de mostrar fecha se convierte automaticamente a str
// dateString:true
// }

// 2. Forma de conectarse a la BD
const conexion = new Sequelize(
  //base datos, usuario, password
  "minimarket",
  "root",
  "root",
  {
    host: "localhost",
    dialect: "mysql",
    timezone: "-05:00",
    logging: false, // para que las consultas no aparezcan en la terminal
    dialectOptions: {
      // al momento de mostrar fecha se convierte automaticamente a str
      dateStrings: true,
    },
  }
);

module.exports = {
  conexion,
};
