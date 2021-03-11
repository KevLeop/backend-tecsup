const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = producto_model = () => {
  return (producto = conexion.define(
    "producto",
    {
      productoId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncrement: true,
        field: "prod_id",
        validate: {
          min: 0,
        },
      },
      productoNombre: {
        type: DataTypes.STRING(45),
        unique: true,
        allowNull: false,
        field: "prod_nombre",
        validate: {
          len: [5, 45],
        },
      },
      productoPrecio: {
        type: DataTypes.FLOAT(5, 2),
        allowNull: false,
        field: "prod_precio",
      },
      productoCantidad: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: "prod_cantidad",
      },
      productoFechaVencimiento: {
        type: DataTypes.DATEONLY,

        allowNull: false,
        field: "prod_fecvec",
        validate: {
          isAfter: "2022-01-01",
        },
      },
      productoEstado: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        field: "prod_estado",
        defaultValue: true,
      },
    },
    {
      tableName: "t_producto",
      timestamps: false,
    }
  ));
};
