const express = require("express");
const app = express();

app.get("/produtos", (req, res) => {
  const produtos = [
    { id: 1, nome: "Notebook", preco: 3500.00 },
    { id: 2, nome: "Mouse", preco: 80.00 }
  ];
  res.json(produtos);
});

app.listen(3000, () => console.log("Servidor rodando em http://localhost:3000"));
