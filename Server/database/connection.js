let mysql = require('mysql');
let connection = {};
connection.init = function(app, config) {
    create(app, config);
}

function create(app, config) {
    var conn = mysql.createConnection({
        host: config.host,
        user: config.user,
        password: config.password,
        database: config.database
    });
    connection.connect();
}

module.exports = connection;