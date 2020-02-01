var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html',
			'Access-Control-Allow-Origin': '*'});
  var data = JSON.parse(fs.readFileSync('./updatedData.json'));
  res.write(JSON.stringify(data))
  res.end();
}).listen(6984);