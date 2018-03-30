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
var validator = require('validator');

const mysql = require('mysql2');
const bcrypt = require('bcrypt')
const saltRounds = 10;


const PYTHONPATH = '/usr/local/opt/python3/bin/python3.6'
var pool  = mysql.createPool({
  host: 'us-cdbr-iron-east-05.cleardb.net',
  user: 'bb47e512244cef',
  password: '50ac0669',
  database: 'heroku_e79dfa0cbc081a3'
});

var getConnection = function(callback) {
  pool.getConnection(function(err, connection) {
      callback(err, connection);
  });
};
connection = {}
connection["execute"] = function() {
  var arg = arguments;
  getConnection(function(err, connect) {

    var argumentList = []
    for (var i = 0; i < arg.length - 1; i++) {
      argumentList.push(arg[i]);
    }
    argumentList.push(function(err, results, fields) {
      arg[arg.length - 1](err, results, fields);
      connect.release();
    })
    // console.log(connect.execute);
    connect.execute.apply(connect, argumentList)   
  })
}


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

// ENCRYPTION STUFF
function hashPassword(pass, callback) {
  bcrypt.genSalt(saltRounds, function(err, salt) {
    bcrypt.hash(pass, salt, function(err, hash) {
      if (err) {
        return callback(true, null);
      }
      callback(null, pass)
    });
  });
}
// UTILS 
function checkCred(user, pass, callback) {
  if (typeof user === 'undefined' || typeof pass === 'undefined') {
    return callback({"valid": false, "reason": "Invalid Credentials"});
  }
  getUser(user, function(result) {
      if (result == null) {
        return callback({"valid": false, "reason": "User does not exist"});
      }
      var pass_hash = result.Password;
      bcrypt.compare(pass ,pass_hash, function(err, res) {
        //will return res of true if passwords are same
        if (err) {
          return callback({"valid": false, "reason": "Invalid Credentials"});
        }
        
        var newresult = {};
        if (res) {
          newresult = {"valid": true}
        } else {
          newresult = {"valid": false, "reason": "Password Incorrect"};
        }
        return callback(newresult)
      });
  });
}

function getUser(user, callback) {
  if (typeof user === 'undefined') {
    return callback(null);
  }
  connection.execute(
    "select * from user where username = ?",
    [user],
    function(err, results, fields) {
      if (err || results.length == 0) {
        return callback(null);
      }
      return callback(results[0]);
    })
}
function deleteUser(username) {
    connection.execute("SET FOREIGN_KEY_CHECKS=0",
    [],
    function(err, results, fields) {
    connection.execute(
      "delete from user where username = ?",
      [username],
      function(err, results, fields) {
        connection.execute(
          "SET FOREIGN_KEY_CHECKS=1",
          [],
          function(err, results, f) {
            console.log("deleted user");
          }
        )
      }
    )
  }
)}
// LOGIN
app.post('/login', function (req, res) {
  var user = req.body.username;
  var pass = req.body.password;
  checkCred(user, pass, function(result) {
    if (result.valid) {
      
      req.session["user"] = user;
      req.session["IsAdmin"] = result.IsAdmin;
      res.send({"status":"SUCCESS"});
    } else {
      res.send({"status":"FAILURE", reason : result.reason  });
    }
  });
});

app.post('/register', function(req, res) {
  var user = req.body.username;
  var pass = req.body.password;
  var breezecard = req.body.breezecard;
  var needNewCard = req.body.needNewCard == "true" ? true : false;
  //make sure pass is right length
  if (pass.length < 8) {
    res.send({"status" : "FAILURE", "reason" : "Password must be eight or more characters"});
    return;
  }
  //check valid email
  if (!validator.isEmail(user)) {
     res.send({"status" : "FAILURE", "reason" : "Please enter a valid email address"});
    return;
  }
  getUser(user, function(result) {
    if (result != null) {
      res.send({"status" : "FAILURE", "reason" : "User already exists"});
      return;
    }
    //now hash pass and store in DB
    bcrypt.genSalt(saltRounds, function(err, salt) {
      bcrypt.hash(pass, salt, function(err, hash) {
          console.log(hash);
          connection.execute(
            //passed all fields, start putting into database wtih User table first
            "insert into user (Username, Password) values (?, ?)",
            [user, hash],
            function(err, results, fields) {
                if (err) {
                  res.send({"status" : "FAILURE", "reason" : "Error in inserting into Users"});
                  deleteUser(user);
                  return;
                }
                console.log("USER ADDED");
            });
      });
    });

  })
});


