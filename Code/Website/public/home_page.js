
const form = document.getElementById('get_data');
const display = document.getElementById('data');
const last_wc = document.getElementById('wc');
const moisture = document.getElementById('moist');
const setpoint = document.getElementById('sp');
const setsetpoint = document.getElementById('ssp')
const temperature = document.getElementById('temp');
const humidity= document.getElementById('hum');
const startDate = document.getElementById('start')
const button = document.getElementById('submit_button');


//Function to retrieve data from JASON file
get_irr_data();

//update data every half a second
setInterval("get_irr_data()", 500);

//get user geolocation
if('geolocation' in navigator){
     console.log('geolocation available');
     navigator.geolocation.getCurrentPosition(async position =>
     {
       const lat = position.coords.latitude;
       const long = position.coords.longitude;
       const head = 'geo'
   
       const data = {head, lat, long};
       const options = {
         method: "POST",
         headers: {
           'Content-Type': 'application/json'
         },
         body: JSON.stringify(data)
       }
       const response = await fetch('/geo', options);
       const resp_data = await response.json();
       console.log(resp_data)  
     });
   }
   else{
     console.log('geolocation unavailable');
   }

function updateTable(jsonData)
{
     last_wc.innerText = jsonData.Irrigation_data.last_watercycle;
     moisture.innerText = jsonData.Irrigation_data.moisture;
     setpoint.innerText = jsonData.Irrigation_data.moisture_setpoint;
     temperature.innerText = jsonData.Irrigation_data.temperature;
     humidity.innerText = jsonData.Irrigation_data.humidity;
     startDate.innerText = jsonData.Irrigation_data.start_data;
}

//Add event listener for submit button
async function send_setpoint()
{
     console.log('Submit pressed');
     const val = setsetpoint.value;
     const head = 'sp'
     const sp = {head, val};
     console.log(sp)
     const options = {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(sp)
        }
     const response = await fetch('/sp', options);
     const resp_data = await response.json();
     console.log(resp_data);

}

async function get_irr_data()
{
     const options = {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
        }
     const response = await fetch('/irr', options);
     const resp_data = await response.json();
     //console.log(resp_data);
     updateTable(resp_data);
}





