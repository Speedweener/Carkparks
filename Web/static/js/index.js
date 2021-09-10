

    const color = {
      0: "#fafa6e",
      1: "#d7f171",
      2: "#b5e877",
      3: "#95dd7d",
      4: "#77d183",
      5: "#5bc489",
      6: "#3fb78d",
      7: "#23aa8f",
      8: "#009c8f",
      9: "#008d8c",
      10: "#007f86",
      11: "#0b717e",
      12: "#1c6373",
      13: "#255566",
      14: "#2a4858",
      15: "#1d6172",

    }

    var polygon_arr = [];
    var polygon_by_weight = [];


    function toLatLong(polygon_with_holes){
        const split_polygon = [];
        for(let part=0; part<polygon_with_holes.length; part++) {
            split_polygon.push(polygon_with_holes[part].map(
                x => new google.maps.LatLng(x[0], x[1])));

        }
        return split_polygon;
    }

    function plotPolygon(polygon_path, map, weight){   
        
        polygon_arr.push(new google.maps.Polygon({
          clickable: false,
          geodesic: true,
          fillColor: color[weight%16],
          fillOpacity: 0.8,
          strokeColor: color[weight%16],
          strokeOpacity: 1.000000,
          strokeWeight: 1,
          map: map,
          paths: polygon_path,
      }));
    }
    function createColorBar(color_bar_values){
        var color_bar = document.getElementById("color-bar");
        
        for(let i=0; i<color_bar_values.length; i++){
          var div = document.createElement('div');
          div.innerHTML = color_bar_values[i];
          div.style.color =  "#000000";

          div.style.backgroundColor = color[i%16];
          div.className = "w3-bar-item w3-hover-red";
          div.addEventListener('mouseenter', e => {
            for(let j=0;j<polygon_by_weight[i].length; j++){
              polygon_arr[polygon_by_weight[i][j]].setOptions({fillColor: "#000000"});
            }


            // mouseTarget.style.border = '5px dotted orange';
            // enterEventCount++;
            // addListItem('This is mouseenter event ' + enterEventCount + '.');
          });

          div.addEventListener('mouseleave', e => {
            for(let j=0;j<polygon_by_weight[i].length; j++){
              polygon_arr[polygon_by_weight[i][j]].setOptions({fillColor: color[i]});
            }


            // mouseTarget.style.border = '5px dotted orange';
            // enterEventCount++;
            // addListItem('This is mouseenter event ' + enterEventCount + '.');
          });

          
          color_bar.appendChild(div)

        }
    }



    function initialize(polygon_values, color_bar_values, lat, long) {

        var map = new google.maps.Map(document.getElementById("map-canvas"), {
            mapTypeId: "satellite",
            zoom: 19,
            center: new google.maps.LatLng(lat, long),

            // mapTypeControl: true,
            // mapTypeControlOptions: {
            //   style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            //   mapTypeIds: ["roadmap", "terrain"],
            // },
        });

        document.getElementById("toggle-plot").addEventListener("click", togglePlot);

        document.getElementById("toggle-lines").addEventListener("click", toggleOutline);

        var slider = document.getElementById("range-slider");

        createColorBar(color_bar_values);
        var color_bar_divs = document.getElementById("color-bar").getElementsByTagName("div");





        // Update the current slider value (each time you drag the slider handle)
        slider.oninput = function() {
          for(let i=0; i<polygon_arr.length;i++){
            polygon_arr[i].setOptions({fillOpacity: parseFloat(this.value) });
          }

          // for(let i=0; i<color_bar_divs.length;i++){
          //   color_bar_divs[i].style.opacity = parseFloat(this.value);
          // }

        }

        var polygon_path;
        var polygon_indexes = [];
        var sum = 0;

        
        for(let weight=0; weight<polygon_values.length; weight++){
            for(let area=0; area<polygon_values[weight].length;area++){
                polygon_indexes.push(sum+area)
                polygon_path = toLatLong(polygon_values[weight][area]);
                plotPolygon(polygon_path, map, weight); 
            }
            sum += polygon_values[weight].length;
            polygon_by_weight.push(polygon_indexes);
            polygon_indexes = [];
        }





    }

   function togglePlot() {

    if(polygon_arr[0].getVisible()){
      for(let i=0; i<polygon_arr.length;i++){
        polygon_arr[i].setVisible(false);
      }


    }
    else{
      for(let i=0; i<polygon_arr.length;i++){
        polygon_arr[i].setVisible(true);
      }

    }
  }

  function toggleOutline() {

    if (document.getElementById('toggle-lines').checked) 
    {
      for(let i=0; i<polygon_arr.length;i++){
        polygon_arr[i].setOptions({strokeOpacity: 1});
      }

    } else {
      
      for(let i=0; i<polygon_arr.length;i++){
        polygon_arr[i].setOptions({strokeOpacity: 0});
      }

    }
  }



   