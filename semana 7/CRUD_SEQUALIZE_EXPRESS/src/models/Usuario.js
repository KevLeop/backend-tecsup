const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");

module.exports = usuario_model = () => {
  let usuario = conexion.define(
    "usuario",
    {
      usuarioId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        allowNull: false,
        autoIncrement: true,
        field: "usu_id",
      },
      usuarioEmail: {
        type: DataTypes.STRING(45),
        field: "usu_email",
        unique: true,
        // https://sequelize.org/master/manual/validations-and-constraints.html
        validate: {
          isEmail: true,
          len: [5, 45],
        },
      },
      usuarioSuperUser: {
        type: DataTypes.BOOLEAN,
        field: "usu_superuser",
        defaultValue: false,
      },
      usuarioPassword: {
        type: DataTypes.TEXT,
        field: "usu_password",
        allowNull: false,
      },
    },
    {
      tableName: "t_usuario",
      timestamps: false,
    }
  );
  return usuario;
};
