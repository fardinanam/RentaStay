String.prototype.isNumber = function() {
    return /^\d+$/.test(this)
}

const roomsCard = document.getElementById('rooms-card')
const rooms = document.getElementById('rooms')
const roomSearchButton = document.getElementById('room-search-btn')
const roomMinicardContainer = document.querySelector('[room-minicard-container]')
const roomMiniCardTemplate = document.querySelector("[room-minicard-template]")

function areValidInputs (checkInDate, checkOutDate, guests) {
    
    if (checkInDate.trim() == '' || checkOutDate.trim() == '' || guests.trim() == '') {
        window.alert('Please fillup the check-in and check-out dates and guests first')
        return false
    } else if(!guests.isNumber()) {
        window.alert('Invalid number of guests')
        return false
    } 

    return true
}

roomSearchButton.onclick = function () {
    const checkInDate = roomsCard.querySelector('#checkIn').value
    const checkOutDate = roomsCard.querySelector('#checkOut').value
    const guests = roomsCard.querySelector('#guestsInput').value
    const noRoom = roomsCard.querySelector('[no-room]')

    if(areValidInputs(checkInDate, checkOutDate, guests)) {
        const info = document.getElementById(["info"])
        const houseId = info.getAttribute("data-house-id")

        roomMinicardContainer.innerHTML = ""

        fetch("/availableRooms/" + houseId + '/' + checkInDate + '/' + checkOutDate + '/' + guests)
        .then(response => response.json())
        .then(rooms => {
            if(rooms.rooms.length != 0) {
                rooms.rooms.forEach(room => {
                    noRoom.classList.add("hide")
                    const roomMiniCard = roomMiniCardTemplate.content.cloneNode(true).children[0]
                    const roomNoText = roomMiniCard.querySelector("[room-no]")
                    const guestsText = roomMiniCard.querySelector("[guests]")
                    const roomPriceText = roomMiniCard.querySelector("[room-price]")
                    const roomReservationButton = roomMiniCard.querySelector("[reservation-button]")

                    const roomNo = room.ROOM_NO

                    roomMiniCard.setAttribute("data-room-no", roomNo)
                    roomNoText.textContent = 'Room No: ' + roomNo
                    guestsText.textContent = room.MAX_CAPACITY + ' guests allowed'
                    roomPriceText.textContent = '$' + room.PRICE
                    roomReservationButton.setAttribute("data-room-no", roomNo)

                    roomReservationButton.onclick = function () {
                        location.href = '/reservation/' + houseId + '/' + roomNo + '/' + checkInDate + '/' + checkOutDate + '/' + guests
                    }

                    roomMinicardContainer.append(roomMiniCard)
                })
            } else {
                noRoom.classList.remove('hide')
                // info.getElementsByTagName('p').textContent = 'No available rooms in this criteria'
            }
        })
    }
}

rooms.querySelectorAll(["button"]).forEach(button => {    
    const houseId = button.getAttribute('id').split('-')[1]
    const roomNo = button.getAttribute('id').split('-')[2]

    button.onclick = function () {
        const checkInDate = roomsCard.querySelector('#checkIn').value
        const checkOutDate = roomsCard.querySelector('#checkOut').value
        const guests = roomsCard.querySelector('#guestsInput').value

        if(areValidInputs(checkInDate, checkOutDate, guests)) {
            location.href = '/reservation/' + houseId + '/' + roomNo + '/' + checkInDate + '/' + checkOutDate + '/' + guests
        }
    }
})



// Date Picker start
var from = $('#checkIn').datepicker({
    dateFormat: "dd-M-yy",
    changeMonth: true,
    changeYear: true,
    minDate: 0
})
.on("change", function() {
    var nextDay = new Date(getDate(this));
    console.log(nextDay)
    nextDay.setDate(nextDay.getDate() + 1);
    to.datepicker("option", "minDate", nextDay)
})

var to = $("#checkOut").datepicker({
    dateFormat: "dd-M-yy",
    changeMonth: true,
    changeYear: true,
    minDate: 0
})
.on("change", function() {
    var prevDay = new Date(getDate(this));
    console.log(prevDay)
    prevDay.setDate(prevDay.getDate() - 1);
    from.datepicker("option", "maxDate", prevDay)
    // from.datepicker("option", "maxDate", getDate(this))

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

