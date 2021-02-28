var input = document.querySelector('.input_text');
var main = document.querySelector('#name-aqi');
var aqi = document.querySelector('#locaqi');
var desc = document.querySelector('.desc');
var clouds = document.querySelector('.clouds');
var button = document.querySelector('.submit');


button.addEventListener('click', function() {
    fetch("http://api.airpollutionapi.com/1.0/aqi?lat=19.04465280219881&lon=72.90984132790611&APPID=p5c97ntv1253a6057han76orif")
        .then(res => res.json())
        .then(data => {
            var namevalue = data['data']['source']['name']
            var aqivalue = data['data']['value']
            var descvalue = data['data']['alert']

            main.innerHTML = namevalue;
            aqi.innerHTML = aqivalue;
            // desc.innerHTML = descvalue;
        })
})