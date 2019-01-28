var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
var util = require("util");
var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "./static")));
app.set("views", path.join(__dirname, "./views"));
app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/submit", (req, res) => {
  let childProcess = require("child_process");
  var process = childProcess.spawn("python", [
    path.resolve() + "\\ml.py",
    req.body.username
  ]);
  process.on("error", err => {
    console.log(err);
    throw err;
  });
  process.stdout.on("data", data => {
    // res.send(data.toString());
    console.log("data      " + data.toString());
    const result = { userdetails: data.toString() };

    res.render("results", result);
  });
});

const port = process.env.PORT || 8000;

app.listen(port, () => {
  let childProcess = require("child_process");
  var process = childProcess.spawn("python", [path.resolve() + "\\ml.py", "1"]);
  process.on("error", err => {
    console.log(err);
    throw err;
  });
  process.stdout.on("data", data => {
    console.log("data      " + data.toString());
  });

  console.log(`running server on  ${port}`);
});
