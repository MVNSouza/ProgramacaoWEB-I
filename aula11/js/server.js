const express = require("express");
const bodyParser = require("body-parser");
const xml2js = require("xml2js");

const app = express();
const builder = new xml2js.Builder();
const parser = new xml2js.Parser({ explicitArray: false });

app.use(bodyParser.json());          // para JSON
app.use(bodyParser.text({ type: "application/xml" })); // para XML cru

let usuarios = [
  { id: 1, nome: "Alice", ativo: true },
  { id: 2, nome: "Bob", ativo: false }
];

// GET com Content Negotiation
app.get("/usuarios", (req, res) => {
  if (req.headers.accept === "application/xml") {
    const xml = builder.buildObject({ usuarios });
    res.type("application/xml").send(xml);
  } else {
    res.json(usuarios);
  }
});

// POST em JSON
app.post("/usuarios", (req, res) => {
  usuarios.push(req.body);
  res.json({ mensagem: "Usuário adicionado", usuario: req.body });
});

// POST em XML
app.post("/usuarios/xml", (req, res) => {
  parser.parseString(req.body, (err, result) => {
    if (err) {
      return res.status(400).send("XML inválido");
    }
    const novoUsuario = result.usuario;
    usuarios.push(novoUsuario);
    res.json({ mensagem: "Usuário adicionado via XML", usuario: novoUsuario });
  });
});

app.listen(3000, () => console.log("Servidor em http://localhost:3000"));
