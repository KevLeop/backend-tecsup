const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = categoria_model = () => {
  return (categoria = conexion.define(
    "categoria",
    {
      categoriaId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncremente: true,
        field: "cat_id",
      },
      categoriaNombre: {
        type: DataTypes.STRING(45),
        unique: true,
        allowNull: false,
        field: "cat_nombre",
      },
    },
    {
      tableName: "t_categoria",
      timestamps: false,
    }
  ));
};
