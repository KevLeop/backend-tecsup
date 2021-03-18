const { conexion } = require("../config/Sequelize");
const {
  Producto,
  Promocion,
  Detalle,
  Cabecera,
  CabeceraNota,
} = require("../config/Creacion");
const moment = require("moment");

const crearVenta = async (req, res) => {
  const { productos, usuario, cliente, serie } = req.body;
  const transaccion = await conexion.transaction();
  // creamos nuestra cabecera de la venta
  try {
    const cabeceraVenta = await CabeceraNota.create(
      {
        cabeceraSerie: "BBB1",
        cabeceraTotal: 0.0,
        cabeceraDescuento: 0.0,
        cabeceraSubTotal: 0.0,
        usu_id: usuario,
        cli_dni: cliente,
      },
      { transaction: transaccion }
    );
    // 1. si el producto tiene promocion
    let descuentoTotal = 0;
    let subTotal = 0;

    for (const key in productos) {
      const { id, cantidad } = productos[key];
      const productoEncontrado = await Producto.findByPk(id, {
        include: {
          model: Promocion,
          order: [["promocionFechaHasta", "DESC"]],
          limit: 1,
        },
      });
      // console.log(producto);
      // console.log(productoEncontrado.toJSON());
      const { promociones } = productoEncontrado;
      console.log(productoEncontrado);
      const fechaActual = new Date();
      let promocionActiva;

      for (const key in promociones) {
        if (fechaActual < promociones[key].promocionFechaHasta) {
          console.log("sigue vigente la promo");
          promocionActiva = promociones[key];
          const descuentoTemporal =
            promociones[key].promocionDescuento * cantidad;
          const precioNormal = productoEncontrado.productoPrecio * cantidad;
          descuentoTotal = descuentoTotal + (precioNormal - descuentoTemporal);
        }
        console.log(promociones[key].toJSON());
      }

      console.log("La promocion activa es: ");
      console.log(promocionActiva);

      const detalleVenta = await Detalle.create(
        {
          detalleCantidad: cantidad,
          detallePrecioUnitario: promocionActiva
            ? promocionActiva.promocionDescuento
            : productoEncontrado.productoPrecio,
          prod_id: id,
          cab_id: cabeceraVenta.cabeceraId,
        },
        { transaction: transaccion }
      );

      await Producto.update(
        {
          productoCantidad: productoEncontrado.productoCantidad - cantidad,
        },
        {
          where: {
            productoId: id,
          },
          transaction: transaccion,
        }
      );
      subTotal += detalleVenta.detallePrecioUnitario * cantidad;
    }

    await CabeceraNota.update(
      {
        cabeceraTotal: subTotal,
        cabeceraSubTotal: subTotal + descuentoTotal,
        cabeceraDescuento: descuentoTotal,
      },
      {
        where: {
          cabeceraId: cabeceraVenta.cabeceraId,
        },
        transaction: transaccion,
      }
    );
    await transaccion.commit();
    return res.status(201).json({
      success: true,
      content: CabeceraNota,
      message: "Se genero la venta exitosamente",
    });
  } catch (error) {
    console.log("Hubo un error");
    console.log(error);
    await transaccion.rollback();
    return res.status(500).json({
      success: false,
      content: error,
      message: "Error al generar la venta",
    });
  }

  return res.send("OK");
  // 2. crear el detalle de la venta
  // 3. restar la cantidad del producto del inventario
  // 4. Agregar el total a la cabecera de la venta
  // 5. Generar la cabecera
  // Nota: se recomienda solamente usar la transaccion en sentencias que modifique nuestra bd
  // (insert, delete, update)
};

// const crearVenta = async (req, res) => {
//   const transaccion = await conexion.transaction();
//   // 1. si el producto tiene promocion
//   let temp = { ...req.body };
//   let { productos } = temp;
//   productos.forEach(async (producto) => {
//     const { id } = producto;
//     const productoEncontrado = await Producto.findByPk(id, {
//       include: { model: Promocion },
//     });
//     // console.log(producto);
//     // console.log(productoEncontrado.toJSON());
//     const { promociones } = productoEncontrado;
//     let { productoPrecio } = productoEncontrado;
//     let precioProd = 0;
//     if (promociones.length > 0) {
//       promociones.forEach((promocion) => {
//         fechaPromoIni = moment(promocion.promocionFechaDesde);
//         fechaPromoFin = moment(promocion.promocionFechaHasta);
//         fechaHoy = moment();
//         // console.log(promocion.toJSON());
//         if (fechaPromoIni < fechaHoy && fechaPromoFin > fechaHoy) {
//           precioProd = promocion.promocionDescuento;
//           console.log(
//             `Promocion: ${promocion.promocionId} esta dentro de la fecha de promocion, monto: ${precioProd}`
//           );
//         } else {
//           console.log(`Promocion: ${promocion.promocionId} no se aplica`);
//           precioProd = productoPrecio;
//         }
//       });
//     } else {
//       precioProd = productoPrecio;
//     }
//     producto["precio"] = precioProd;

//     console.log(`Producto no tiene promociones`);
//     return res.json(temp);

//     // console.log(productoEncontrado.toJSON());
//     // TAREA!!!: indicar si es que tiene promocion activa dar ese precio,
//     // caso contrario dar el precio original del producto
//   });
//   // 2. crear el detalle de la venta
//   // 3. restar la cantidad del producto del inventario
//   // 4. Agregar el total a la cabecera de la venta
//   // 5. Generar la cabecera
//   // Nota: se recomienda solamente usar la transaccion en sentencias que modifique nuestra bd
//   // (insert, delete, update)
// };

module.exports = {
  crearVenta,
};
