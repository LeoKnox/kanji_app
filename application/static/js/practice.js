function nextKanji(x) {
    y = Math.floor(Math.random()*x.length);
    document.getElementById("kanji_row").innerHTML = "\
        <td>"+x[y][1]+"</td>\
        <td>"+x[y][3]+"</td>\
        <td>"+x[y][4]+"</td>\
        <td>"+x[y][5]+"</td>\
        <td>"+x[y][6]+"</td>";
}