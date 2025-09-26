const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Servidor rodando com Node.js!');
});

server.listen(3000, () => {
  console.log('Servidor no ar: http://localhost:3000');
});
