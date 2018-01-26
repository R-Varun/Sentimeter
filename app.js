var bodyParser = require('body-parser')
var express = require('express')
var app = express()
var port = process.env.PORT || 3000;
var path = require('path');
var server = require('http').createServer(app);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
var config = require('./config.js');
const session = require('express-session')
var uniqid = require("uniqid");
const pug = require('pug');
var viewPath = path.join(__dirname, 'views');
var fs = require('fs');
var needle = require('needle');
const saltRounds = 10;

//Templating ----x`
app.set('views', './views');
app.set('view engine', 'pug');
//Session ----
app.use(session({
    secret: 'secret key xd',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
  }));
app.use(express.static('public'))
// var redis = require('redis');

app.get("/", function(req, res) {
    res.sendFile('html/index.html' , { root : __dirname});
});
app.get("/input.html", function(req, res) {
  res.sendFile('html/input.html' , { root : __dirname});
});
app.get("/results.html", function(req, res) {
  res.sendFile('html/results.html' , { root : __dirname});
});

app.get("/loader.html", function(req, res) {
  res.sendFile('html/loader.html' , { root : __dirname});
});


server.listen(port, function () {
  console.log("server running on port: " + port.toString())
})
