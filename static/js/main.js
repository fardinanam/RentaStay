console.log("Ashche");

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

const addHtmlToElement = (element,html) => {
    element.innerHTML = html;
}

const fetchResultState = value => {
    if(value){
        console.log(value);
        const url = `/accounts/fetch_states/${value}/`;
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
                html+=`<option value="{{ ${d} }}">{{ ${d} }}</option>`
            }
            addHtmlToElement(statename,html);
        })
        .catch(err => {
            console.log(err);
        })
    }
    else{
        let html='';
        html += `<option selected="true" disabled="disabled">State Name</option>`;
        addHtmlToElement(statename,html);
    }
};

const checkForState = value => {
    console.log("Value: "+value);
    if(value=="Country Name"){
        alert("Please select a country first");
    }
    else if(value){
        console.log(value);
        const url = `/accounts/fetch_states/${value}/`;
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

const checkForCity = (value1,value2) => {
    console.log("Value: "+value1 +" value: " + value2);
    if(value1=="Country Name" && value2=="State Name"){
        alert("Please select a country first");
    }
    else if(value1!="Country Name" && value2=="State Name"){
        alert("Please select a state");
    }
}

statename.onclick = () => checkForState(countryname.value);
//statename.onchange = () => fetchResultState(countryname.value);
cityname.onclick = () => checkForCity(countryname.value, statename.value);


