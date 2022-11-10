const colorCode = {
  0:  "#040c4e", 
  1:  "#071051", 
  2:  "#0a1555",
  3:  "#0d1a58",
  4:  "#111e5c",
  5:  "#142360",
  6:  "#172863",
  7:  "#1b2d67",
  8:  "#1e316a",
  9:  "#21366e",
  10:  "#253b72",
  11:  "#284075",
  12:  "#2b4479",
  13:  "#2e497c",
  14:  "#324e80",
  15:  "#355384",
  16:  "#385787",
  17:  "#3c5c8b",
  18:  "#3f618f",
  19:  "#426592",
  20:  "#466a96",
  21:  "#496f99",
  22:  "#4c749d",
  23:  "#5078a1",
  24:  "#537da4",
  25:  "#5682a8",
  26:  "#5987ab",
  27:  "#5d8baf",
  28:  "#6090b3",
  29:  "#6395b6",
  30:  "#679aba",
  31:  "#6a9ebd",
  32:  "#6da3c1",
  33:  "#71a8c5",
  34:  "#74acc8",
  35:  "#77b1cc",
  36:  "#7bb6d0",
  37:  "#7ebbd3",
  38:  "#81bfd7",
  39:  "#84c4da",
  40:  "#88c9de",
  41:  "#8bcee2",
  42:  "#8ed2e5",
  43:  "#92d7e9",
  44:  "#95dcec",
  45:  "#98e1f0",
  46:  "#9ce5f4",
  47:  "#9feaf7",
  48:  "#a2effb",
  49:  "#a6f4ff", 
  50:  "#b2dee6", 
  51:  "#bec9cd",
  52:  "#cbb3b5",
  53:  "#d79e9c",
  54:  "#e48884",
  55:  "#f0736b",
  56:  "#fd5e53", 
  57:  "#ed5852", 
  58:  "#dd5352",
  59:  "#ce4e52",
  60:  "#be4951",
  61:  "#af4451",
  62:  "#9f3f51",
  63:  "#903a50",
  64:  "#803550",
  65:  "#702f50",
  66:  "#612a4f",
  67:  "#51254f",
  68:  "#42204f",
  69:  "#321b4e",
  70:  "#23164e",
  71:  "#13114e",
  72:  "#040c4e"


}


const fillColours = {
  2: "#ff0000",
  1: "#D81515",
  0: "#A01717", 
  3: "#26F107",
  4: "#32D319",
  5: "#2AA017",
}


// GLOBALS
var plot = [];

let map;
const circles = [[0, 1.448589660573756, 103.82115670293068],
[1, 1.363142385867216, 103.89226406553928],
[2, 1.3827982265943584, 103.7672235415534],
[3, 1.2855097099078496, 103.81119850873618],
[4, 1.385717992827047, 103.74561764224984],
[5, 1.3519701721108013, 103.95333322076216],
[6, 1.2822935795524406, 103.83065321951237],
[7, 1.3864684913608887, 103.88461760624985],
[8, 1.3365859188533349, 103.85320441757544],
[9, 1.3171685778764957, 103.76025042272727],
[10, 1.3722695248835357, 103.9535980234044],
[11, 1.313627700939746, 103.85880399409666],
[12, 1.3433085287709694, 103.70837268236983],
[13, 1.4256079021333752, 103.83922481281905],
[14, 1.304923504115193, 103.79580902691832],
[15, 1.3195681661444114, 103.88265827177516],
[16, 1.3676153904566077, 103.8448288497331],
[17, 1.3290026380847866, 103.93114624442494],
[18, 1.3630701941356094, 103.87269087335741],
[19, 1.3485372874333466, 103.7445921244842],
[20, 1.3171594201156653, 103.90727806393146],
[21, 1.393175796309999, 103.90699315484736],
[22, 1.3540211230519217, 103.93565459382386],
[23, 1.4380416142220613, 103.79031978467165],
[24, 1.4041145183619266, 103.9009029615997]
]
// 0.009 = 1km



function initializeMap(colorBarValues, predictedValues) {

  map = new google.maps.Map(document.getElementById("map_canvas"), {

    mapTypeId: "satellite",
    zoom: 12,
    center: new google.maps.LatLng(1.3416894022651873, 103.82354635457985),

  });


  let infoWindow = new google.maps.InfoWindow();

  map.addListener("click", (mapsMouseEvent) => {

    infoWindow.close();
    
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });

    infoWindow.setContent(
      "<p>" +
      "<b>Lat</b>: " + mapsMouseEvent.latLng.lat() + "<br />" +
      "<b>Long</b>: " + mapsMouseEvent.latLng.lng() +
      "</p>"
    );

    infoWindow.open(map);
  });


  for (let x in circles) {
    plotCircle(circles[x][1], circles[x][2]);
  }
  createColorBar(colorBarValues, predictedValues);


  
}




function updateMap(colorBarValues, predictedValues) {
  clearMap();

  for (let x in circles) {
    plotCircle(circles[x][1], circles[x][2]);
  }
  createColorBar(colorBarValues, predictedValues);

}

function checkMapUndefined() {
  return map === undefined;
}

function clearMap() {
  for (let i = 0; i < plot.length; i++) {
    plot[i].setMap(null);
  }

  plot = [];
}





// Returns LatLng coordinates of polygon split into outer polygon (part = 0) and holes (other parts)
function toLatLong(polygonValues) {
  const polygonPath = [];
  for (let part = 0; part < polygonValues.length; part++) {
    polygonPath.push(polygonValues[part].map(
      x => new google.maps.LatLng(x[0], x[1])));
  }
  return polygonPath;
}


function plotCircle(lat, long) {
  plot.push(new google.maps.Circle({
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.5,
    map: map,
    center: new google.maps.LatLng(lat, long) ,
    radius: 0,

  }));
}


function createColorBar(colorBarValues, predictedValues) {
  const colorBar = document.getElementById("color_bar");

  // Clear previous colour bar if any
  while (colorBar.firstChild) {
    colorBar.removeChild(colorBar.lastChild);
  }


  for (let i = 0; i < colorBarValues.length; i++) {
    var div = document.createElement('div');
    div.innerHTML = colorBarValues[i];
    div.style.color = "#000000";

    div.style.backgroundColor = colorCode[i % 72];
    div.style.height = "3px";
    div.className = "w3-bar-item w3-hover-red";
    div.addEventListener('mouseenter', e => {
      
      for (let j = 0; j < plot.length; j++) {
        plot[j].setOptions({ radius: predictedValues[i][j]});
        plot[j].setOptions({ fillColor: 
          fillColours[(predictedValues[i][j] >700)? 2 : (predictedValues[i][j] >350) ? 1 : (predictedValues[i][j] >0) ? 0:
          (predictedValues[i][j] < -700)? 3 : (predictedValues[i][j] < -350) ? 4 : 5] });
        plot[j].setOptions({ strokeColor: 
          fillColours[(predictedValues[i][j] >700)? 2 : (predictedValues[i][j] >350) ? 1 : (predictedValues[i][j] >0) ? 0:
          (predictedValues[i][j] < -700)? 3 : (predictedValues[i][j] < -350) ? 4 : 5] });

          // console.log(predictedValues[i][j]);
      }
    });
    colorBar.appendChild(div)

  }
}






