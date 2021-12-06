const Express = require("express")();
const HttpExpress = require("http").Server(Express);
const http = require("http");
const Socketio = require("socket.io")(HttpExpress);
const fs = require("fs");

const err404 = "404: No Page Found";

const markers = [];

http.createServer(function(req, res) {
    res.setHeader("X-Content-Type-Options", "nosniff");
    Socketio.on("connection", socket => {
        for(let i = 0; i < markers.length; i++) {
            socket.emit("marker", markers[i]);
        }
        socket.on("marker", data => {
            markers.push(data);
            Socketio.emit("marker", data);
        });
    });
    console.log(markers);
    if (req.url == "/") {
        console.log("wtf");
        fs.readFile("./pages/live_map.html", function(err, html) {
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

// Socketio.on("connection", socket => {
//     for(let i = 0; i < markers.length; i++) {
//         socket.emit("marker", markers[i]);
//     }
//     socket.on("marker", data => {
//         markers.push(data);
//         Socketio.emit("marker", data);
//     });
// });

HttpExpress.listen(3000, () => {
    console.log("Listening at :3000...");
});