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
        }).appendTo(".fly");
    });
}

function comparer(index, type) {
    if (type == 'Name') {
        return function(a, b) {
            var valA = getCellValue(a, index)
            var valB = getCellValue(b, index)
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

function splitURLS(){
    var urls = document.querySelectorAll(".url")
    function formatUrl(r){
        return r.split("//").map(
            r=>r.replace(/(?<after>:)/giu,"$1<wbr>"
                ).replace(/(?<before>[/~.,\-_?#%])/giu,"<wbr>$1"
                ).replace(/(?<equals>=)/giu,"<wbr>$1<wbr>"
                ).replace(/(?<ampersand>&amp;)/giu,"<wbr>&<wbr>"
            )).join("//<wbr>")
    }
    urls.forEach(r=>{
        var e=formatUrl(r.innerHTML)
        return r.innerHTML=`${e}`
    })
}

$(document).on('click','.clicky',function(){
    var table = $(this).parents('table').eq(0)
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index(),$(this).text()))
    this.asc = !this.asc
    if (this.asc){rows = rows.reverse()}
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
})

document.addEventListener('DOMContentLoaded', function() {
    printEmoji();
    splitURLS();
}, false);

$(document).on('click','.refs > a',function() {
    var h=$(this).attr("href"),h=$(h)
    $(".ref-highlight").removeClass("ref-highlight")
    h.addClass("ref-highlight")
})
