const pedido = {
  id: 1001,
  cliente: {
    id: 1,
    nome: "Alice"
  },
  itens: [
    { produto: "Notebook", quantidade: 1, preco: 3500.00 },
    { produto: "Mouse", quantidade: 2, preco: 80.00 }
  ]
};

// Serializar
const jsonPedido = JSON.stringify(pedido, null, 2);
console.log(jsonPedido);

// Desserializar
const obj = JSON.parse(jsonPedido);
console.log("Cliente:", obj.cliente.nome);
console.log("Itens:", obj.itens.length);
