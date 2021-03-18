const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = detalle_model = () => {
  return conexion.define(
    "detalles",
    {
      detalleId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncrement: true,
        field: "det_id",
      },
      detalleCantidad: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: "det_cantidad",
      },
      detallePrecioUnitario: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "det_precunit",
      },
    },
    {
      tableName: "t_det_nota",
      timestamps: false,
    }
  );
};
