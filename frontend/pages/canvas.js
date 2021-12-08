const socket = new WebSocket('ws://' + window.location.host + '/websocket');

window.addEventListener("load",() => {

    //var map = document.getElementById("map");
    var canvas = document.getElementById("canvas");
    var img = new Image(1379, 974);
    img.src = 'images/northCampus.png'
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    let painting = false;

    function startPosition(e){
        painting = true;
        draw(e);
    }

    function finishedPosition(){
        painting = false;
        ctx.beginPath();
    }
    socket.onmessage = receiveDraw;

    function receiveDraw(data) {
        console.log(data.data)
        var coords = JSON.parse(data.data)
        console.log(coords);
        var x = coords.x
        var y = coords.y
        console.log('Receving: ' + x + ' and ' + y);
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function draw(e){
        if(!painting) return;

        console.log('Sending: ' + e.clientX + ' and ' + e.clientY);

        var data = {
            x: e.clientX,
            y: e.clientY
        }
        socket.send(JSON.stringify(data));
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';

        ctx.lineTo(e.clientX, e.clientY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX, e.clientY);

    }

    canvas.addEventListener("mousedown",startPosition);
    canvas.addEventListener("mouseup",finishedPosition);
    canvas.addEventListener("mousemove",draw);
});