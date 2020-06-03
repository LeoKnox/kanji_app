function nextKanji(x) {
    y = Math.floor(Math.random()*x.length);
    document.getElementById("kanji_row").innerHTML = "\
        <td>"+x[y][1]+"</td>\
        <td>"+x[y][3]+"</td>\
        <td>"+x[y][4]+"</td>\
        <td>"+x[y][5]+"</td>\
        <td>"+x[y][6]+"</td>";
}

function drawStroke(e) {
    var x = e.clientX;
    var y = e.clientY;
    var coor = "Coordinates: (" + x + "," + y + ")";
    document.addEventListener("mousemove", mm);
    //document.getElementById("")
}

function mm(e) {
    var x = e.clientX;
    var y = e.clientY;
    var svg = document.getElementById('draw');
    var point = svg.createSVGPoint();
    drawStroke(e);
    //document.getElementById("")
    var offset = document.getElementById('draw').getBoundingClientRect();
    point.x +=(x);
    point.y +=(y - Math.floor(offset.top));
    console.log(offset.top);
    var polyline = document.getElementById('polypoint');
    polyline.points.appendItem(point);
}

function clearCoor() {
    document.getElementById('polypoint').id="";
    document.getElementById('draw').innerHTML += '<polyline id="polypoint" points="" style="fill:none;stroke:#000000;stroke-width:6" />';
    document.removeEventListener('mousemove', mm)
}