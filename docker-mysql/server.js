var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "alpruser",
  password: "=[-p0o9i8U",
  database: "alprdata"

});

con.connect(function (err) {
  if (err) throw err;
  var sqlTable = `CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            plate TEXT,
            uuid TEXT,
            img TEXT
          )`
  var alprInsert = "INSERT INTO alpr (plate, uuid) VALUES ?";
  var  sql = "INSERT INTO customers (name, address) VALUES ('Company Inc', 'Highway 37')";

  con.query(sqlTable, function (err, result) {
    if (err) throw err;
  });

  con.query(sql, function (err, result) {
    if (err) throw err;
  });

});

