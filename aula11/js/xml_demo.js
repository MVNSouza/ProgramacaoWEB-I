// Importa a biblioteca
const xml2js = require("xml2js");

// Construtor para serializar
const builder = new xml2js.Builder();

// Objeto JS
const usuario = { usuario: { id: 1, nome: "Alice", ativo: true } };

// Serialização: objeto -> XML
const xml = builder.buildObject(usuario);
console.log("XML serializado:\n", xml);

// Parser para desserializar
const parser = new xml2js.Parser({ explicitArray: false });

parser.parseString(xml, (err, result) => {
  if (err) {
    console.error("Erro ao parsear XML:", err);
  } else {
    console.log("Objeto desserializado:", result);
    console.log("Nome do usuário:", result.usuario.nome);
  }
});