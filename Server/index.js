const http = require('http');
const express = require('express');

const app = express();
http.createServer(app);

var router = express.Router();
var bodyParser = require('body-parser');
var ejs = require("ejs-locals");

var db = require('./database');


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: false
}));

app.engine('ejs', ejs);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname + '/views'));

var index = require('./routes/')(router);

app.use('/', index);

module.exports = app;