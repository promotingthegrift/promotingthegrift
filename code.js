function printEmoji() {
    $('.celeb').each(function () {
        var x = (Math.floor(Math.random()*94)+1).toString().concat("%");
        var y = (Math.floor(Math.random()*94)+1).toString().concat("%");
        var o = ((Math.random()*25)+5)/100;
        $("<span>💸</span>").addClass(
            "money"
        ).css({
            "opacity":o,
            "bottom":x,
            "left":y
        }).appendTo("body");
    });
}

function comparer(index, type) {
    if (type == 'Name') {
        return function(a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index)
            return valA.toString().localeCompare(valB)
        }
    } else if (type == 'Est. worth ($)') {
        return function(a, b) {
            var valA = getCellValue(a, index).trim().replace('*','').replace(/,/g,'')
            var valB = getCellValue(b, index).trim().replace('*','').replace(/,/g,'')
            return valA - valB
        }
    } else if (type == 'Date') {
        return function(a, b) {
            var valA = Date.parse(getCellValue(a, index))
            var valB = Date.parse(getCellValue(b, index))
            return valA - valB
        }
    }
}

function getCellValue(row, index){
    return $(row).children('td').eq(index).text()
}

$(document).on('click','.clicky',function(){
    var table = $(this).parents('table').eq(0)
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index(),$(this).text()))
    this.asc = !this.asc
    if (this.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
})
