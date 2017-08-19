const http = require('http');
const express = require('express');

const app = express();
http.createServer(app);

var router = express.Router();
var bodyParser = require('body-parser');
var ejs = require("ejs-locals");
var config = require('./config');
var mysql = require('mysql');

var path = require('path');
var fs = require('fs');
var session = require('express-session');

app.use(session({
    secret: 'qwerty1234',
    resave: false,
    saveUninitialized: true,
    cookie: {
        maxAge: 600000
    }
}));

var port = 3000;

var connection = mysql.createConnection({
    host: config.host,
    user: config.user,
    port: config.port,
    password: config.password,
    database: config.database
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: false
}));

app.use(express.static((path.join(__dirname, 'public'))));

app.engine('ejs', ejs);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname + '/views'));

var index = require('./routes/')(router, connection);
var api = require('./routes/api')(router, connection);

app.use('/', index);
app.use('/api', api);

app.listen(port, () => {
    console.log("server on!");
});

module.exports = app;