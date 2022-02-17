String.prototype.isNumber = function() {
    return /^\d+$/.test(this)
}

// Reservation button start
const roomsCard = document.getElementById('rooms-card')

roomsCard.querySelectorAll(["button"]).forEach(button => {    
    const houseId = button.getAttribute('id').split('-')[1]
    const roomNo = button.getAttribute('id').split('-')[2]

    button.onclick = function () {
        const checkInDate = roomsCard.querySelector('#checkIn').value
        const checkOutDate = roomsCard.querySelector('#checkOut').value
        const guests = roomsCard.querySelector('#guestsInput').value

        if(!guests.isNumber()) {
            window.alert('Invalid number of guests')
        } else if(checkInDate.trim() != '' && checkOutDate.trim() != '' && guests.trim() != '') {
            location.href = '/reservation/' + houseId + '/' + roomNo + '/' + checkInDate + '/' + checkOutDate + '/' + guests
        } else {
            window.alert('Please fillup the check0in and check-out dates and guests first')
        }
    }
})

// Date Picker start
console.log("date picker")
var from = $('#checkIn').datepicker({
    dateFormat: "dd-M-yy",
    changeMonth: true,
    changeYear: true,
    minDate: 0
})
.on("change", function() {
    to.datepicker("option", "minDate", getDate(this))
})

var to = $("#checkOut").datepicker({
    dateFormat: "dd-M-yy",
    changeMonth: true,
    changeYear: true
})
.on("change", function() {
    from.datepicker("option", "maxDate", getDate(this))
})

function getDate(element) {
    var date
    let dateFormat = "dd-M-yy"
    try{
        date = $.datepicker.parseDate(dateFormat, element.value)
    } catch(error) {
        date = null
    }

    return date
}
// Date picker end

