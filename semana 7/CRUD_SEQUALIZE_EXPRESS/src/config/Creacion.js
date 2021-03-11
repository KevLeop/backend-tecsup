const categoria_model = require("../models/Categoria");
const cliente_model = require("../models/Cliente");
const usuario_model = require("../models/Usuario");
const cabecera_model = require("../models/Cabecera");
const producto_model = require("../models/Producto");
const detalle_model = require("../models/Detalle");
const promocion_model = require("../models/Promocion");

// si usamos algun parametro del sync en la conexion se ejecutara para todas los modelos que tengamos registrado en nuestro proyecto (CUIDADO!!!)
// dentro del sync se puede passar un parametro con dos llaves:
// force => va a resetear toda la tabla o bd, va a borrar toda su configuracion y va a crear todo de 0, se perdera toda la data correspondiente (internamente hace un drop table y un create table if not exists)
// alter => verifica que los modelos esten igual que las tablas en al bd y si hay algun cambio como tipo de dato, nombre de columna, etc solamente hara ese cambio mas no reseteará la(s) tabla(s) como lo hace el force, (internamente hace un alter table)
// basta con llamar al modelo este se encargara de su creacion
// .sync({ force: true })
const Categoria = categoria_model();
const Cliente = cliente_model();
const Usuario = usuario_model();
const CabeceraNota = cabecera_model();
const Producto = producto_model();
const Detalle = detalle_model();
const Promocion = promocion_model();

Usuario.hasMany(CabeceraNota, {
  foreignKey: { name: "usu_id", allowNull: false },
});
CabeceraNota.belongsTo(Usuario, { foreignKey: "usu_id" });

Cliente.hasMany(CabeceraNota, {
  foreignKey: { name: "cli_dni", allowNull: false },
});
CabeceraNota.belongsTo(Cliente, { foreignKey: "cli_dni" });

Producto.hasMany(Detalle, {
  foreignKey: { name: "prod_id", allowNull: false },
});
Detalle.belongsTo(Producto, { foreignKey: "prod_id" });

Producto.hasMany(Promocion, {
  foreignKey: { name: "prod_id", allowNull: false },
});
Promocion.belongsTo(Producto, { foreignKey: "prod_id" });

CabeceraNota.hasMany(Detalle, {
  foreignKey: { name: "cab_id", allowNull: false },
});
Detalle.belongsTo(CabeceraNota, { foreignKey: "cab_id" });

Categoria.hasMany(Producto, {
  foreignKey: { name: "cat_id", allowNull: false },
});
Producto.belongsTo(Categoria, { foreignKey: "cat_id" });

module.exports = {
  Categoria,
  Cliente,
  Usuario,
  CabeceraNota,
  Producto,
  Detalle,
  Promocion,
};
