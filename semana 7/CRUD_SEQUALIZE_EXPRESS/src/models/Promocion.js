const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = promocion_model = () => {
  return conexion.define(
    "promocion",
    {
      promocionId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncrement: true,
        field: "prom_id",
      },
      promocionFechaDesde: {
        type: DataTypes.DATE,
        allowNull: false,
        field: "prom_fecdesde",
      },
      promocionFechaHasta: {
        type: DataTypes.DATE,
        allowNull: false,
        field: "prom_fechasta",
      },
      promocionDescuento: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "prom_descuento",
      },
      promocionEstado: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        field: "prom_estado",
      },
    },
    {
      tableName: "t_promocion",
      timestamps: false,
    }
  );
};
