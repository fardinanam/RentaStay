console.log("date picker")
var from = $('#checkIn').datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true,
    minDate: 0
})
.on("change", function() {
    to.datepicker("option", "minDate", getDate(this))
})

var to = $("#checkOut").datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true
})
.on("change", function() {
    from.datepicker("option", "maxDate", getDate(this))
})

function getDate(element) {
    var date
    let dateFormat = "dd-mm-yy"
    try{
        date = $.datepicker.parseDate(dateFormat, element.value)
    } catch(error) {
        date = null
    }

    return date
}