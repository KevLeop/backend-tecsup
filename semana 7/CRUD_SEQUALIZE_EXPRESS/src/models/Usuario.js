const { DataTypes } = require("sequelize");
const { conexion } = require("../config/Sequelize");
const bcrypt = require("bcrypt");
const { sign } = require("jsonwebtoken");

module.exports = usuario_model = () => {
  let usuario = conexion.define(
    "usuarios",
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
  /* Aqui ira la encriptacion de la contraseña */
  // al momento de usar el prototype estamos agregando nuevas funcionalidades
  // a nuestro objeto usuario para que puedan ser usadas como el findAll(), build(),etc.
  // estas podrán ser accedidas desde cualquier lado de la app
  usuario.prototype.setearPassword = async function (password) {
    const hash = bcrypt.hashSync(password, 10);
    // const hash = await bcrypt
    //   .hash(password, 10)
    //   .catch((error) => console.log(error));
    this.usuarioPassword = hash;
  };

  usuario.prototype.validarPassword = function (password) {
    // COMPARA LA CONTRASEÑA QUUE se le provee con el hash almacenado y si son iguales
    // retornara verdadero, caso contraro retorna falso
    return bcrypt.compareSync(password, this.usuarioPassword);
  };

  usuario.prototype.generarJWT = function () {
    // primero creamos el payload (que es la parte que el front puede visualizar con normalidad en la TOKEN)
    const payload = {
      usuarioId: this.usuarioId,
      usuarioEmail: this.usuarioEmail,
    };
    // Luego declaro la firma para encriptar la
    const password = process.env.JWT_SECRET || "password";
    // una vez que ya tenemos definido el payload
    return sign(payload, password, { expiresIn: "1h" }, { algorithm: "RS256" });
  };

  return usuario;
};
