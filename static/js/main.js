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
const houseId = document.getElementById('houseid');
const addHousePicBtn = document.getElementById('addHousePicBtn');
const addPicBtn = document.getElementById('addBtnHouse');
const addRoomBtn = document.getElementById('addRoomBtn');


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
        addPicBtn.style.display="block";
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
            //console.log(noOfHouse)
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
        })
        .catch(err => {
            console.log(err);
        })
    }
}

try{
    addHousePicBtn.onclick = () => addNewHousePic();
}
catch{
    //console.log("On house preview page!!");
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

