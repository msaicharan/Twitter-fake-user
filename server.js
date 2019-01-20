var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
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
  const oldSpawn = childProcess.spawn;
  const mySpawn = () => {
    console.log("arguments passed are " + JSON.stringify(arguments));
    var result = oldSpawn.apply(this, arguments);
    return result;
  };
  childProcess.spawn = mySpawn;

  var process = childProcess.spawn("py", [
    __dirname + "\\model.py",
    req.body.username
  ]);
  process.on("error", function(err) {
    throw err;
  });
  process.stdout.on("data", function(data) {
    // res.send(data.toString());
    const res = { result: data.toString() };
    res.render("results", res);
  });
});

app.listen(8000, () => {
  console.log("listening on port 8000");
});
