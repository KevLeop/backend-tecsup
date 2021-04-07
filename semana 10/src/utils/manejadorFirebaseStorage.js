const { Storage } = require("@google-cloud/storage");

const storage = new Storage({
  projectId: "prueba-firebase-kevin",
  keyFilename: "./credenciales-firebase.json",
});

// luuego se crea la variable BUCKET que se usa como referencia al link del storage
// ! No se crea el protocolo, solo despues del doble slash '//'
const bucket = storage.bucket("prueba-firebase-kevin.appspot.com");

const subirArchivo = (archivo) => {
  return new Promise((resolve, reject) => {
    // validamos que exista un archivo, si no existe, REJECT!
    if (!archivo) reject("No se encontro el archivo");
    // comenzamos a cargar el archivo mediante su nombre
    const fileUpload = bucket.file(archivo.originalname);
    // agregamos la configuracion adicional de nuestro archivo a subir,
    // como por ejemplo su metadata
    const blobStream = fileUpload.createWriteStream({
      metadata: {
        contentType: archivo.mimetype,
      },
    });
    // si hay un error al momento de subir el archivo ingresaremos a su estado error
    blobStream.on("error", (error) => {
      reject("Hubo un error al subir el archivo: ${error}");
    });
    // si el archivo termino de subirse correctamente ingresaremos a su estado finish
    blobStream.on("finish", () => {
      fileUpload
        .getSignedUrl({
          action: "read",
          expires: "04-10-2021", // MM-DD-YYYY
        })
        .then((link) => resolve(link))
        .catch((error) => reject(error));
    });
    //aqui es donde se culmina el proceso de subida de imagenes
    // se le manda el buffer del archivo(bytes del archivo)
    blobStream.end(archivo.buffer);
  });
};

const eliminarArchivo = async (nombreArchivo) => {
  try {
    const rpta = await bucket.file(nombreArchivo).delete();
    console.log(rpta);
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
};

module.exports = { subirArchivo, eliminarArchivo };
