function initializeMap(){
    var earth = new WE.map('earth_div');
    earth.setView([53, -124], 2);
    
    var layer = WE.tileLayer('https://api.mapbox.com/styles/v1/starswap/ciwqktlti00282qldewk9ouvu/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoic3RhcnN3YXAiLCJhIjoiY2l3cWVpaHp0MDAwYzJ3bGxvNmFzbWtxZiJ9.DdzWiexFsKv0ghcxEJXPvQ');
    layer.addTo(earth);
    
    addMarker([53,-123], earth);
}

function addMarker(coords, earth){
    var marker = WE.marker(position = coords, iconUrl = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png', width = 32, height = 32).addTo(earth)
}

//var marker = WE.marker([51.5, -0.1]).addTo(earth)
//marker.bindPopup('<b>Hello world!</b>');