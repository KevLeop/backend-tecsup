const { DataTypes } = require("sequelize");

const categoria_model = (conexion) => {
  return (categoria = conexion.define("categoria", {
    categoriaId: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      allowNull: false,
      autoIncremente: true,
      field: "cat_id",
    },
  }));
};
