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
const deletePicBtn = document.getElementById('deletePicBtn');


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

try{
    deletePicBtn.onclick = () => setImageSession();
}
catch{
    //console.log("On edit house page!!");
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

