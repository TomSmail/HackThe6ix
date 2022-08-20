
function initializeMap(){
    var earth = new WE.map('earth_div');
    // Centres on British Columbia
    earth.setView([53, -124], 2);
    
    var layer = WE.tileLayer('https://api.mapbox.com/styles/v1/starswap/ciwqktlti00282qldewk9ouvu/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoic3RhcnN3YXAiLCJhIjoiY2l3cWVpaHp0MDAwYzJ3bGxvNmFzbWtxZiJ9.DdzWiexFsKv0ghcxEJXPvQ');
    layer.addTo(earth);
    var coords2DArray = [[52.826007, -125.193972], [52.829602, -125.189244], [52.826980, -125.188556], [52.824476, -125.188672], [52.822698, -125.190879]];
    const centreCoord = findCentreOfCoords(coords2DArray);
    addZone(coords2DArray, earth,'#ff0000');
    addMarker(centreCoord, earth);
}

function addMarker(coords, earth){
    var droneMarker = WE.marker(position = coords, iconUrl = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png', width = 32, height = 32).addTo(earth);
}

function addZone(coords2DArray, earth, color){
    var options = {color: color, opacity: 1, fillColor: '#ff0000', fillOpacity: 0.25, weight: 1};
    var polygon = WE.polygon(coords2DArray, options).addTo(earth);
}

function findCentreOfCoords(coords2DArray){
    let totalXCoords = 0;
    let totalYCoords = 0;
    for (let i = 0; i < coords2DArray.length; i++){
        totalXCoords += coords2DArray[i][0];
        totalYCoords += coords2DArray[i][1];
    }
    const centreCoord  = [totalXCoords/coords2DArray.length, totalYCoords/coords2DArray.length];
    console.log(centreCoord);
    return centreCoord;
}


//var marker = WE.marker([51.5, -0.1]).addTo(earth)
//marker.bindPopup('<b>Hello world!</b>');