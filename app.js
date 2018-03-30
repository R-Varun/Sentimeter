var bodyParser = require('body-parser')
var express = require('express')
var app = express()
var port = process.env.PORT || 3000;
var path = require('path');
var server = require('http').createServer(app);

var config = require('./config.js');
const session = require('express-session')
var uniqid = require("uniqid");
const pug = require('pug');
var viewPath = path.join(__dirname, 'views');
var fs = require('fs');
var needle = require('needle');
var PythonShell = require('python-shell');
var utils = require("./utils.js");
const saltRounds = 10;

// const PYTHONPATH = '/usr/local/opt/python3/bin/python3.6'


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

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
app.get("/input", function(req, res) {
  res.sendFile('html/input.html' , { root : __dirname});
});
app.get("/login", function(req, res) {
  res.sendFile('html/login.html' , { root : __dirname});
});

app.post("/user/data", async function(req, res) {
  if (typeof req.session["session-data"] === 'undefined') {
    res.send({status : "ERROR", message : "NO DATA AVAILABLE"});
  } else {
    res.send({status : "SUCCESS", data: req.session["session-data"]});
  }

});

app.post('/api/analyze',async function (req, res) {
  var data = req.body;
  // validate input for analyze bloc
  // console.dir(data);


  var valid = await utils.validateInput(data)
  // if (!valid) {
  //   res.send({status : "ERROR", message : "FORMAT INVALID"})
  //   return;
  // }

  // data["corpus"] = "";
  
  var ars =  [JSON.stringify(data)]
  
  console.log(ars)
  PythonShell.run('python/main.py' , {mode:"json", args:ars}, function (err, results) {
    if (err) {
        
        console.log("PYTHON FAILED");
        res.send({status : "ERROR", message : "PYTHON SCRIPT FAILED"})
        throw err;
        return        
    }

    var dataObj = {}
    dataObj = results[0]
    dataObj["stride"] = data["stride"]
    dataObj["len"] = data["data"].length;
    req.session["session-data"] = dataObj

    console.log(results);
    res.send(results);
    return;
  });

  // utils.validateInput(data).then((ans) => {
  //   console.log(ans);
  //   // res.send(ans);
  //   if (ans == false) {
  //     res.send({status : "ERROR", message : "FORMAT INVALID"})
  //     return;
  //   } else {
  //     PythonShell.run('test.py' , ["lol"], function (err, results) {
  //       if (err) {
  //           console.log(err);
  //       }
  //       // results is an array consisting of messages collected during execution
  //       fileID = results[0];

  //       // want to send a response of the link here

  //       res.send(fileID);
  //       return;
  //       // res.send({"file":'/gifs/'+fileID + ".gif"})
  //   });

  //   }
  // })
});

function error(err) {
  console.log(err);
}



app.get("/results.html", function(req, res) {
  res.sendFile('html/results.html' , { root : __dirname});
});


app.get("/feature", function(req, res) {
  res.sendFile('html/feature.html' , { root : __dirname});
});


app.get("/loader.html", function(req, res) {
  res.sendFile('html/loader.html' , { root : __dirname});
});





server.listen(port, function () {
  console.log("server running on port: " + port.toString())
})
