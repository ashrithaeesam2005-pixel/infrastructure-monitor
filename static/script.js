let detectedIssue = "";
let userLocation = "";
let map;

/* LOAD MAP AFTER PAGE LOAD */

window.onload = function(){

    if(navigator.geolocation){

        navigator.geolocation.getCurrentPosition(function(position){

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            userLocation = lat + "," + lon;

            map = L.map('map').setView([lat, lon], 15);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            L.marker([lat, lon]).addTo(map)
            .bindPopup("Your Location")
            .openPopup();
            loadComplaints();

        });

    }

};
async function loadComplaints(){

    const response = await fetch("/get_reports");

    const reports = await response.json();

    reports.forEach(function(report){

        if(report.location){

            const coords = report.location.split(",");

            const lat = parseFloat(coords[0]);
            const lon = parseFloat(coords[1]);

            L.marker([lat, lon]).addTo(map)
            .bindPopup(
                "Complaint ID: " + report.id +
                "<br>Issue: " + report.issue +
                "<br>Status: " + report.status
            );

        }

    });

}


/* IMAGE PREDICTION */

document.getElementById("uploadForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const fileInput = document.getElementById("imageInput");

    const formData = new FormData();

    formData.append("image", fileInput.files[0]);

    const response = await fetch("/predict", {
        method:"POST",
        body:formData
    });

    const data = await response.json();

    detectedIssue = data.prediction;

    document.getElementById("predictionResult").innerText =
        "Detected Issue: " + detectedIssue;

    document.getElementById("generateComplaint").style.display = "block";

});


/* GENERATE COMPLAINT */

document.getElementById("generateComplaint").addEventListener("click", async function(){

    const response = await fetch("/generate_complaint", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            issue: detectedIssue,
            location: userLocation
        })

    });

    const data = await response.json();

    document.getElementById("complaintText").value = data.complaint;

    document.getElementById("submitComplaint").style.display = "block";

});


/* SUBMIT REPORT */

document.getElementById("submitComplaint").addEventListener("click", async function(){

    const response = await fetch("/submit_report", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            issue: detectedIssue,
            location: userLocation
        })

    });

    const data = await response.json();

    alert(
        "Complaint Submitted Successfully\nComplaint ID: "
        + data.complaint_id
    );

});


/* CHECK STATUS */

async function checkStatus(){

    const complaintId =
        document.getElementById("complaintIdInput").value;

    const response =
        await fetch("/check_status/" + complaintId);

    const data = await response.json();

    if(data.status){

        document.getElementById("statusResult").innerText =
        "Issue: " + data.issue +
        " | Location: " + data.location +
        " | Status: " + data.status;

    }

    else{

        document.getElementById("statusResult").innerText =
        "Complaint not found";

    }

}