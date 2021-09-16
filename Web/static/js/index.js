const colorCode = {
  0: "#ffff07",
  1: "#eafc20",
  2: "#d6f92f",
  3: "#c2f63c",
  4: "#aff248",
  5: "#9cee52",
  6: "#8ae95c",
  7: "#77e465",
  8: "#65de6e",
  9: "#51d976",
  10: "#3dd37d",
  11: "#23cd83",
  12: "#00c789",
  13: "#00c08d",
  14: "#00ba91",
  15: "#00b394",
  16: "#00ac96",
  17: "#00a697",
  18: "#009f98",
  19: "#009897",
  20: "#009195",
  21: "#008a92",
  22: "#00828e",
  23: "#147b89",
  24: "#247483",
  25: "#2f6d7d",
  26: "#366776",
  27: "#3c606e",
  28: "#405966",
  29: "#42535d",

  // 0: "#fafa6e",
  // 1: "#d7f171",
  // 2: "#b5e877",
  // 3: "#95dd7d",
  // 4: "#77d183",
  // 5: "#5bc489",
  // 6: "#3fb78d",
  // 7: "#23aa8f",
  // 8: "#009c8f",
  // 9: "#008d8c",
  // 10: "#007f86",
  // 11: "#0b717e",
  // 12: "#1c6373",
  // 13: "#255566",
  // 14: "#2a4858",
  // 15: "#1d6172",

}

// GLOBALS
var plot = [];
var plotByWeight = [];
let map;

function initializeMap(polygonValues, colorBarValues, lat, long) {

  map = new google.maps.Map(document.getElementById("map_canvas"), {
    mapTypeId: "satellite",
    zoom: 19,
    center: new google.maps.LatLng(lat, long),

    // mapTypeControl: true,
    // mapTypeControlOptions: {
    //   style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
    //   mapTypeIds: ["roadmap", "terrain"],
    // },
  });

  document.getElementById("toggle_plot").addEventListener("click", togglePlot);

  document.getElementById("toggle_lines").addEventListener("click", toggleOutline);

  var slider = document.getElementById("range_slider");
  // Update the current slider value (each time you drag the slider handle)
  slider.oninput = function () {
    for (let i = 0; i < plot.length; i++) {
      plot[i].setOptions({ fillOpacity: parseFloat(this.value) });
    }
  }

  createColorBar(colorBarValues);

  var polygonIndexes = [];
  var sum = 0;

  for (let weight = 0; weight < polygonValues.length; weight++) {
    for (let area = 0; area < polygonValues[weight].length; area++) {
      polygonIndexes.push(sum + area)
      plotPolygon(toLatLong(polygonValues[weight][area]), weight);
    }
    sum += polygonValues[weight].length;
    plotByWeight.push(polygonIndexes);
    polygonIndexes = [];
  }
}

function checkMapUndefined() {
  return map === undefined;
}

function clearMap() {
  for (let i = 0; i < plot.length; i++) {
    plot[i].setMap(null);
  }
  plot = [];
  plotByWeight = [];
}


function updateMap(polygonValues, colorBarValues, lat, long) {
  clearMap();

  if (!document.getElementById("toggle_fix").checked) {
    map.setCenter(new google.maps.LatLng(lat, long));
  }


  createColorBar(colorBarValues);

  var polygonIndexes = [];
  var sum = 0;

  for (let weight = 0; weight < polygonValues.length; weight++) {
    for (let area = 0; area < polygonValues[weight].length; area++) {
      polygonIndexes.push(sum + area)
      plotPolygon(toLatLong(polygonValues[weight][area]), weight);
    }
    sum += polygonValues[weight].length;
    plotByWeight.push(polygonIndexes);
    polygonIndexes = [];
  }
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


// Plots polygons with color matching its weight. "polygon_path" can consists of several list, corresponding to the holes of the polygon
function plotPolygon(polygonPath, weight) {
  plot.push(new google.maps.Polygon({
    clickable: false,
    geodesic: true,
    fillColor: colorCode[weight % 30],
    fillOpacity: document.getElementById("range_slider").value,
    strokeColor: colorCode[weight % 30],
    strokeOpacity: 1.000000,
    strokeWeight: 1,
    map: map,
    paths: polygonPath,
  }));
}

function createColorBar(colorBarValues) {
  const colorBar = document.getElementById("color_bar");

  // Clear previous colour bar if any
  while (colorBar.firstChild) {
    colorBar.removeChild(colorBar.lastChild);
  }


  for (let i = 0; i < colorBarValues.length; i++) {
    var div = document.createElement('div');
    div.innerHTML = colorBarValues[i];
    div.style.color = "#000000";

    div.style.backgroundColor = colorCode[i % 30];
    div.className = "w3-bar-item w3-hover-red";
    div.addEventListener('mouseenter', e => {
      for (let j = 0; j < plotByWeight[i].length; j++) {
        plot[plotByWeight[i][j]].setOptions({ fillColor: "#000000" });
      }
    });

    div.addEventListener('mouseleave', e => {
      for (let j = 0; j < plotByWeight[i].length; j++) {
        plot[plotByWeight[i][j]].setOptions({ fillColor: colorCode[i] });
      }
    });


    colorBar.appendChild(div)

  }
}

function togglePlot() {
  if (plot[0].getVisible()) {
    for (let i = 0; i < plot.length; i++) {
      plot[i].setVisible(false);
    }
  } else {
    for (let i = 0; i < plot.length; i++) {
      plot[i].setVisible(true);
    }
  }
}

function toggleOutline() {
  if (document.getElementById('toggle_lines').checked) {
    for (let i = 0; i < plot.length; i++) {
      plot[i].setOptions({ strokeOpacity: 1 });
    }

  } else {
    for (let i = 0; i < plot.length; i++) {
      plot[i].setOptions({ strokeOpacity: 0 });
    }
  }
}



