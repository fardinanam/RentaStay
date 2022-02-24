String.prototype.isNumber = function() {
    return /^\d+$/.test(this)
}

$(function () {
    'use strict';
    // Showing page loader
    $(window).on('load', function () {
        setTimeout(function () {
            $(".page_loader").fadeOut("fast");
        }, 200);
   });

    $('.hideMessage').on('click',function(){
        document.getElementById("message").style.display = "None";
    });

    // Slick Sliders
    $('.slick-carousel').each(function () {
        var slider = $(this);
        $(this).slick({
            infinite: true,
            dots: false,
            arrows: false,
            centerMode: true,
            centerPadding: '0'
        });
        
        $(this).closest('.slick-slider-area').find('.slick-prev').on("click", function () {
            slider.slick('slickPrev');
        });
        $(this).closest('.slick-slider-area').find('.slick-next').on("click", function () {
            slider.slick('slickNext');
        });
    });
});

setTimeout(function(){
    $('#message').fadeOut('slow');
}, 4000);

const countryname = document.getElementById('countryname');
const statename = document.getElementById('statename');
const cityname = document.getElementById('cityname');
const addHousePic = document.getElementById('addHousePic');
const addRoomPic = document.getElementById('addRoomPic');
const houseId = document.getElementById('houseid');
const roomHouseId = document.getElementById('roomhouseid');
const roomNumberId = document.getElementById('roomnumberid');
const addHousePicBtn = document.getElementById('addHousePicBtn');
const addBtnHouse = document.getElementById('addBtnHouse');
const addRoomPicBtn = document.getElementById('addRoomPicBtn');
const addBtnRoom = document.getElementById('addBtnRoom');
const addRoomBtn = document.getElementById('addRoomBtn');
const picLimit = document.getElementById('picLimit');
const popupheading = document.getElementById('popupheading');
const popupmessage = document.getElementById('popupmessage');
const udform = document.getElementById('udform');

const imgDiv = document.querySelector('.profile-pic-div');
const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadBtn = document.querySelector('#uploadBtn');

const addHtmlToElement = (element,html) => {
    element.innerHTML = html;
}

const changeCityName = value => {
    let html='';
    html += `<option selected="true" disabled="disabled">City Name</option>`;
    addHtmlToElement(cityname,html);
};

const changeCityAndStateNames = value => {
    let html='';
    html += `<option selected="true" disabled="disabled">State Name</option>`;
    addHtmlToElement(statename,html);
    html='';
    html += `<option selected="true" disabled="disabled">City Name</option>`;
    addHtmlToElement(cityname,html);
};

const checkForStateNames = value => {
    //console.log("Value: "+value);
    if(value=="Country Name"){
        alert("Please select a country first");
    }
    else if(value && statename.value=="State Name"){
        //console.log(value);
        const url = `/accounts/fetch_statenames/${value}/`;
        fetch(url, {
            method: "GET"
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            data.sort();
            let html='';
            html += `<option selected="true" disabled="disabled">State Name</option>`;
            for(let d of data){
                html+=`<option value="${d}">${d}</option>`
            }
            addHtmlToElement(statename,html);
        })
        .catch(err => {
            console.log(err);
        })
    }
}

const checkForCityNames = (value1,value2) => {
    //console.log("Value: "+value1 +" value: " + value2);
    if(value1=="Country Name" && value2=="State Name"){
        alert("Please select a country first");
    }
    else if(value1!="Country Name" && value2=="State Name"){
        alert("Please select a state");
    }
    else if(value1!="Country Name" && value2!="State Name" && cityname.value=="City Name"){
        const url = `/accounts/fetch_citynames/${value1}/${value2}/`;
        fetch(url, {
            method: "GET"
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            data.sort();
            let html='';
            html += `<option selected="true" disabled="disabled">City Name</option>`;
            for(let d of data){
                html+=`<option value="${d}">${d}</option>`
            }
            addHtmlToElement(cityname,html);
        })
        .catch(err => {
            console.log(err);
        })
    }
}

const addNewHousePic = value => {
    if(addHousePicBtn.disabled != true){
        addHousePicBtn.disabled = true;
        let idOfHouse = houseId.value 
        const url = `/accounts/fetch_no_of_house_pics/${idOfHouse}/`;
        fetch(url, {
            method: "GET"
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            let noOfHouse = data[0]
            if(noOfHouse==5){
                picLimit.style.display="block";
            }
            else{
                //console.log(noOfHouse)
                addBtnHouse.style.display="block";
                var c=1;
                var brk = document.createElement("span");
                brk.innerHTML="<br>";
                addHousePic.appendChild(brk);
                for (var input = noOfHouse+1; input <= 5; input++) {
                    var newHousePicLabel = document.createElement("label");
                    newHousePicLabel.for = "upload"+input;
                    newHousePicLabel.innerHTML="House Pic " + c + ":";
                    newHousePicLabel.style="padding-left: 5%;"
                    addHousePic.appendChild(newHousePicLabel);
                    var newHousePic = document.createElement("input");
                    newHousePic.type="file";
                    newHousePic.accept="image/*";
                    newHousePic.name="upload"+input;
                    newHousePic.style="padding-left: 5%;"
                    addHousePic.appendChild(newHousePic);
                    var brk = document.createElement("span");
                    brk.innerHTML="<br><br>";
                    addHousePic.appendChild(brk);
                    c++;
                }
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
}

const addNewRoomPic = value => {
    if(addRoomPicBtn.disabled != true){
        addRoomPicBtn.disabled = true;
        let idOfHouse = roomHouseId.value 
        let roomno = roomNumberId.value
        const url = `/accounts/fetch_no_of_room_pics/${idOfHouse}/${roomno}/`;
        fetch(url, {
            method: "GET"
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            let noOfHouse = data[0]
            if(noOfHouse==5){
                picLimit.style.display = "block";
            }
            else{
                addBtnRoom.style.display="block";
                //console.log(noOfHouse)
                var c=1;
                var brk = document.createElement("span");
                brk.innerHTML="<br>";
                addRoomPic.appendChild(brk);
                for (var input = noOfHouse+1; input <= 5; input++) {
                    var newRoomPicLabel = document.createElement("label");
                    newRoomPicLabel.for = "uploadroom"+input;
                    newRoomPicLabel.innerHTML="Room Pic " + c + ":";
                    newRoomPicLabel.style="padding-left: 5%;"
                    addRoomPic.appendChild(newRoomPicLabel);
                    var newRoomPic = document.createElement("input");
                    newRoomPic.type="file";
                    newRoomPic.accept="image/*";
                    newRoomPic.name="uploadroom"+input;
                    newRoomPic.style="padding-left: 5%;"
                    addRoomPic.appendChild(newRoomPic);
                    var brk = document.createElement("span");
                    brk.innerHTML="<br><br>";
                    addRoomPic.appendChild(brk);
                    c++;
                }
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
}


$(document).ready(function(){
    $(".simg").magnificPopup({
        type : 'image',
        gallery : {
            enabled: true
        }
    });
})

//Pop up functionality start

if(udform!=null){
    udform.addEventListener('submit', function ( event ) {
        console.log("paise")
        event.preventDefault();
    });
}

//<form action="{% url 'home' %}" method="post" id="udform">
//    {% csrf_token %}
//    <input type="submit" value="Submit" onclick="onUDClick('ho','matha','{{csrf_token}}','homeyes')">
//</form>

function onUDClickRoom(header, msg, csrf_token, postmsg, urlpage,houseid,roomno){
    console.log(postmsg)
    Confirm.open({
        title: header,
        message: msg,
        onok: () => {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": csrf_token },
                url: urlpage,
                data: {
                    "YES" : postmsg,
                    "house_id" : houseid,
                    "roomnumber": roomno
                },
                success: function(data){
                    console.log(data.url)
                    window.location.href=data.url
                },
                dataType: "json"
            });
            return false;
        }
    })
}

function onUDClickHouse(header, msg, csrf_token, postmsg, urlpage,houseid){
    console.log(postmsg)
    Confirm.open({
        title: header,
        message: msg,
        onok: () => {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": csrf_token },
                url: urlpage,
                data: {
                    "YES" : postmsg,
                    "house_id": houseid
                },
                success: function(data){
                    console.log(data.url)
                    window.location.href=data.url
                },
                dataType: "json"
            });
            return false;
        }
    })
}


function onUDClickUser(header, msg, csrf_token, postmsg, urlpage){
    console.log(postmsg)
    Confirm.open({
        title: header,
        message: msg,
        onok: () => {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": csrf_token },
                url: urlpage,
                data: {
                    "YES" : postmsg,
                },
                success: function(data){
                    console.log(data.url)
                    window.location.href=data.url
                },
                dataType: "json"
            });
            return false;
        }
    })
}

const Confirm = {
    open (options) {
        options = Object.assign({}, {
            title: '',
            message: '',
            okText: 'Continue',
            cancelText: 'Cancel',
            onok: function () {},
            oncancel: function () {}
        }, options);
        
        const html = `
            <div class="confirm">
                <div class="confirm__window">
                    <div class="confirm__titlebar">
                        <span class="confirm__title">${options.title}</span>
                        <button class="confirm__close">&times;</button>
                    </div>
                    <div class="confirm__content">${options.message}</div>
                    <div class="confirm__buttons">
                        <button class="confirm__button confirm__button--ok confirm__button--fill">${options.okText}</button>
                        <button class="confirm__button confirm__button--cancel">${options.cancelText}</button>
                    </div>
                </div>
            </div>
        `;

        const template = document.createElement('template');
        template.innerHTML = html;

        // Elements
        const confirmEl = template.content.querySelector('.confirm');
        const btnClose = template.content.querySelector('.confirm__close');
        const btnOk = template.content.querySelector('.confirm__button--ok');
        const btnCancel = template.content.querySelector('.confirm__button--cancel');

        confirmEl.addEventListener('click', e => {
            if (e.target === confirmEl) {
                options.oncancel();
                this._close(confirmEl);
                console.log('Returning false');
                //return false;
            }
        });

        btnOk.addEventListener('click', () => {
            options.onok();
            this._close(confirmEl);
            console.log('Returning true');
            //return true;
        });

        [btnCancel, btnClose].forEach(el => {
            el.addEventListener('click', () => {
                options.oncancel();
                this._close(confirmEl);
                console.log('Returning false');
               // return false;
            });
        });

        document.body.appendChild(template.content);
    },

    _close (confirmEl) {
        confirmEl.classList.add('confirm--close');

        confirmEl.addEventListener('animationend', () => {
            document.body.removeChild(confirmEl);
        });
    }
};

//Pop up end

// Profile image upload function start
if(file != null) {
    file.addEventListener('change', function(){
    //this refers to file
        const choosedFile = this.files[0];
        if (choosedFile) {
            const reader = new FileReader(); 
            reader.addEventListener('load', function(){
                img.setAttribute('src', reader.result);
            });
            reader.readAsDataURL(choosedFile);
        }
    });
}



try{
    addHousePicBtn.onclick = () => addNewHousePic();
}
catch{
    //console.log("On house preview page!!");
}

try{
    addRoomPicBtn.onclick = () => addNewRoomPic();
}
catch{
    //console.log("On room preview page!!");
}

try{
    statename.onclick = () => checkForStateNames(countryname.value);
    statename.onchange = () => changeCityName();
    countryname.onchange = () => changeCityAndStateNames();
    cityname.onclick = () => checkForCityNames(countryname.value, statename.value);
}
catch{
    //console.log("On add home page!!")
}

const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

if(openModalButtons != null && overlay != null && closeModalButtons != null) {
    openModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = document.querySelector(button.dataset.modalTarget)
            openModal(modal)
        })
    })

    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal-custom.active')
        modals.forEach(modal => {
            closeModal(modal)
        })
    })

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal-custom')
            const cardBody = modal.closest('.card-body')
            const ownerStar = modal.querySelector("[star-select-owner]")
            const houseStar = modal.querySelector("[star-select-house]")
            const ownerReview = modal.querySelector("[owner-review-input]")
            const houseReview = modal.querySelector("[house-review-input]")
            const rentId = modal.getAttribute("data-rent-id") 
            const cardOwnerRating = cardBody.querySelector("[card-owner-rating]")
            const cardHouseRating = cardBody.querySelector("[card-house-rating]")
            const cardOwnerReview = cardBody.querySelector("[card-owner-review]")
            const cardHouseReview = cardBody.querySelector("[card-house-review]")
            
            let url = "/updateReview/" + rentId + '/' + ownerStar.value + '/' + houseStar.value + '/' + ownerReview.value + '/' + houseReview.value
            fetch(url)
            .then(response => response.json)
            .then(data => {
                console.log(data)
                
                cardOwnerRating.innerHTML = ownerStar.value
                cardOwnerReview.innerHTML = ownerReview.value
                cardHouseRating.innerHTML = houseStar.value
                cardHouseReview.innerHTML = houseReview.value
            })
            closeModal(modal)
        })
    })

    function openModal(modal) {
        if (modal == null) return
        modal.classList.add('active')
        overlay.classList.add('active')
    }

    function closeModal(modal) {
        if (modal == null) return
        modal.classList.remove('active')
        overlay.classList.remove('active')
    }
}
