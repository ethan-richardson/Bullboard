const http = require("http");
const fs = require("fs");

const err404 = "404: No Page Found";

console.log("starting server!")
http.createServer(function(req, res) {
    res.setHeader("X-Content-Type-Options", "nosniff");
    if (req.url == "/") {
        fs.readFile("./login.html", function(err, html) {
            if (err) {
                res.writeHead(404, {
                    "Content-Length": Buffer.byteLength(err404),
                    "Content-Type": "text/plain"
                })
                res.end(err404);
            }
            else {
                res.writeHead(200, {
                    "Content-Length": Buffer.byteLength(html),
                    "Content-Type": "text/html"
                });
                res.end(html);
            }
        });
    }
    else if (req.url == "/styles.css") {
        fs.readFile("./styles.css", function(err, css) {
            if (err) {
                res.writeHead(404, {
                    "Content-Length": Buffer.byteLength(err404),
                    "Content-Type": "text/plain"
                })
                res.end(err404);
            }
            else {
                res.writeHead(200, {
                    "Content-Length": Buffer.byteLength(css),
                    "Content-Type": "text/css"
                });
                res.end(css);
            }
        });
    }
    else if (req.url == "/bull_knocker.jpeg") {
        fs.readFile("./bull_knocker.jpeg", function(err, bull_knocker) {
            if (err) {
                res.writeHead(404, {
                    "Content-Length": Buffer.byteLength(err404),
                    "Content-Type": "text/plain"
                })
                res.end(err404);
                console.log("dog no worky");
            }
            else {
                res.writeHead(200, {
                    "Content-Length": Buffer.byteLength(bull_knocker),
                    "Content-Type": "image/jpeg"
                });
                res.end(bull_knocker);
                console.log("bull worky :D");
            }
        })
    }
    else {
        res.writeHead(404, {
            "Content-Length": Buffer.byteLength(err404),
            "Content-Type": "text/plain"
        })
        res.end(err404);
    }
}).listen(8000);
