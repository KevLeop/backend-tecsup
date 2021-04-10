const socket = io("http://127.0.0.1:5000");

socket.on("connect", () => {
  console.log("conectado");
});

function setup() {
  createCanvas(400, 300);
  background(0);
  socket.on("coordenadas", (data) => {
    fill(0, 0, 255);
    noStroke();
    ellipse(data.x, data.y, 15, 15);
  });
}

function mouseDragged() {
  fill(112, 239, 65);
  ellipse(mouseX, mouseY, 10, 10);
  noStroke();
  enviarPunto(mouseX, mouseY);
}

const enviarPunto = (posX, posY) => {
  console.log(`x: ${posX} y: ${posY}`);
  const data = {
    x: posX,
    y: posY,
  };
  socket.emit("coordenada", data);
};
