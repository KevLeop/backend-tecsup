const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = cabecera_model = () => {
  return conexion.define(
    "cabecera",
    {
      cabeceraId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncrement: true,
        field: "cab_id",
      },
      cabeceraFecha: {
        type: DataTypes.DATEONLY,
        allowNull: false,
        field: "cab_fecha",
      },
      cabeceraSerie: {
        type: DataTypes.STRING(4),
        allowNull: false,
        field: "cab_serie",
      },
      cabeceraTotal: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "cab_total",
      },
      cabeceraDescuento: {
        type: DataTypes.STRING(45),
        allowNull: false,
        field: "cab_dscto",
      },
      cabeceraSubTotal: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "cab_subtotal",
      },
    },
    {
      tableName: "t_cab_nota",
    }
  );
};
