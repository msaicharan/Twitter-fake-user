var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
var util = require('util')
var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "./static")));
app.set("views", path.join(__dirname, "./views"));
app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/submit", (req, res) => {
  // let childProcess = require("child_process");
  // const oldSpawn = childProcess.spawn;
  // const mySpawn = () => {
  //   //console.log(util.inspect(arguments))
  // //  console.log(JSON.stringify(arguments));
  //   var result = oldSpawn.apply(this, arguments);
  //   return result;
  // };
  // childProcess.spawn = mySpawn;

  var process = require("child_process").spawn("python", [
    __dirname + "\\ml.py",
    req.body.username
  ]);
  process.on("error", (err) =>{
    console.log(err);
    throw err;
  });
  process.stdout.on("data", (data)=> {
    // res.send(data.toString());
    console.log("data      "+data.toString());
    const result = { result: data.toString() };

    res.render("results", result);
  });
});

app.listen(8000, () => {
  console.log("listening on port 8000");
  // childProcess.spawn = mySpawn;

  // var process = require("child_process").spawn("python", [
  //   __dirname + "\\ml.py","1"]);
});
