
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)

})


function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: {lat: lat_b, lng: long_b}
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

// const waypts = [
//         {location: {lat: lat_b, lng: long_b},
//         stopover: true},
//         {location: {lat: lat_d, lng: long_d},
//         stopover: true}
//         ];
function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: origin,
        destination: destination,
        // waypoints: waypts,
        optimizeWaypoints: false,
        travelMode: google.maps.TravelMode.DRIVING,
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);


      } else {

        alert('Directions request failed due to ' + status);
        window.location.assign("/map")
      }
    });
}

function addItem() {
  const tbody = document.getElementById("table_body");
  var itemName = document.getElementById("itemName").value;
  var quantity = document.getElementById("quantity").value;
  var width = document.getElementById("width").value;
  var height = document.getElementById("height").value;
  var depth = document.getElementById("depth").value;
  var type_measurement = document.getElementById("type_measurement").value;
  var weight = document.getElementById("weight").value;
  var type_weight = document.getElementById("type_weight").value;
  var x = document.getElementById("stored_value").value;
  var y = document.getElementById("existing_items").value;
  var volume = width * height * depth;




  // <tr> </tr>
  if ((itemName != "") && (quantity != "") && (width != "") && (height != "") && (depth != "") && (weight != "")){

    // Assigning item to the string of existing items
    document.getElementById("existing_items").value = y + "," + x;

    const new_tr_item = document.createElement("tr");

    new_tr_item.setAttribute('id','id-' + x.toString());

    const new_th_itemName = document.createElement("th");
    new_th_itemName.setAttribute('scope','row');
    new_th_itemName.textContent = itemName;
    new_th_itemName.setAttribute('id','id-itemName-' + x.toString());
    new_th_itemName.setAttribute('value',itemName);
    new_tr_item.appendChild(new_th_itemName);

    const new_td_quantity = document.createElement("td");
    new_td_quantity.textContent = quantity;
    new_td_quantity.setAttribute('id','id-quantity-' + x.toString());
    new_td_quantity.setAttribute('value',quantity);
    new_tr_item.appendChild(new_td_quantity);

    const new_td_width = document.createElement("input");
    new_td_width.textContent = width.toString();
    new_td_width.setAttribute('id','id-width-' + x.toString());
    new_td_width.setAttribute('value',width);
    new_td_width.setAttribute('type','hidden');
    new_tr_item.appendChild(new_td_width);

    const new_td_height = document.createElement("input");
    new_td_height.textContent = height.toString();
    new_td_height.setAttribute('id','id-height-' + x.toString());
    new_td_height.setAttribute('value',height);
    new_td_height.setAttribute('type','hidden');
    new_tr_item.appendChild(new_td_height);

    const new_td_depth = document.createElement("input");
    new_td_depth.textContent = depth.toString();
    new_td_depth.setAttribute('id','id-depth-' + x.toString());
    new_td_depth.setAttribute('value',depth);
    new_td_depth.setAttribute('type','hidden');
    new_tr_item.appendChild(new_td_depth);

    const new_td_volume = document.createElement("td");
    new_td_volume.textContent = volume.toString() + ' ' + type_measurement + '3';
    new_td_volume.setAttribute('id','id-volume-' + x.toString());
    new_td_volume.setAttribute('value',volume);
    new_td_volume.setAttribute('class','hide_item');
    new_tr_item.appendChild(new_td_volume);

    const new_td_weight = document.createElement("td");
    new_td_weight.textContent = weight.toString() + ' ' + type_weight;
    new_td_weight.setAttribute('id','id-weight-' + x.toString());
    new_td_weight.setAttribute('value',weight);
    new_td_weight.setAttribute('class','hide_item');
    new_tr_item.appendChild(new_td_weight);

    const new_td_typemeasurement = document.createElement("input");
    new_td_typemeasurement.textContent = type_measurement;
    new_td_typemeasurement.setAttribute('id','id-typemeasurement-' + x.toString());
    new_td_typemeasurement.setAttribute('value',type_measurement);
    new_td_typemeasurement.setAttribute('type','hidden');
    new_tr_item.appendChild(new_td_typemeasurement);

    const new_td_typeweight = document.createElement("input");
    new_td_typeweight.textContent = type_weight;
    new_td_typeweight.setAttribute('id','id-typeweight-' + x.toString());
    new_td_typeweight.setAttribute('value',type_weight);
    new_td_typeweight.setAttribute('type','hidden');
    new_tr_item.appendChild(new_td_typeweight);

    const new_td_remove = document.createElement("td");
    const new_remove_button = document.createElement("button");
    new_remove_button.setAttribute('class','btn btn-primary form-control')
    new_remove_button.setAttribute('onClick','removeItem(' + '"id-' + x.toString() + '")')
    new_remove_button.textContent = 'remove item';
    new_td_remove.appendChild(new_remove_button);
    new_tr_item.appendChild(new_td_remove);

    tbody.appendChild(new_tr_item);

    // adding +1 to stored_value
    x = parseInt(x) + 1;
    // toggle/untoogle no items
    var existing_items = document.getElementById("existing_items").value
    if (existing_items === ''){
      document.getElementById('noitems').innerText = 'No items'
    } else {
      document.getElementById('noitems').innerText = ''
    }


    document.getElementById("stored_value").value = x;
    document.getElementById("itemName").value = "";
    document.getElementById("quantity").value = "";
    document.getElementById("width").value = "";
    document.getElementById("height").value = "";
    document.getElementById("depth").value = "";
    document.getElementById("weight").value = "";
    var warning = document.getElementById("warnings");
    warning.textContent = "";
    document.getElementById("stored_value_warning").value = "0";
  } else {
    const warning_exist = document.getElementById("stored_value_warning").value;
    if (warning_exist == '0'){
      var warning = document.getElementById("warnings");
      warning.textContent = "Please fill out the blank spaces.";
    }

  }

}

function removeItem(x) {
  const tbody = document.getElementById("table_body");
  const item_to_remove = document.getElementById(x);
  tbody.removeChild(item_to_remove);

  var y = x.slice(3);
  console.log('y');
  console.log(y);
  var z = document.getElementById("existing_items").value;

  var splited_string = z.split(",");
  var index = splited_string.indexOf(y);
  if (index > -1) {
    splited_string.splice(index, 1);
  }
  document.getElementById("existing_items").value = splited_string.toString();
  // toggle/untoogle no items
  var existing_items = document.getElementById("existing_items").value
  if (existing_items === ''){
    document.getElementById('noitems').innerText = 'No items'
  } else {
    document.getElementById('noitems').innerText = ''
  }
}

function submitform() {
  var string = '';
  var y = document.getElementById("existing_items").value;
  var array = y.split(',');
  var i = 0;

  while (i < array.length) {
    if (array[i] === "") {
      array.splice(i, 1);
    } else {
      ++i;
    }
  }
  console.log(array)
  for (let x = 0; x < array.length; x++) {
    var string_one = document.getElementById("id-itemName-" + array[x]).innerText
    string += string_one.toString() + ";;";
    var string_two = document.getElementById("id-quantity-" + array[x]).innerText
    string += string_two.toString() + ";;";
    var string_three = document.getElementById("id-width-" + array[x]).innerText
    string += string_three.toString() + ";;";
    var string_four = document.getElementById("id-height-" + array[x]).innerText
    string += string_four.toString() + ";;";
    var string_five = document.getElementById("id-depth-" + array[x]).innerText
    string += string_five.toString() + ";;";
    var string_seven = document.getElementById("id-typemeasurement-" + array[x]).innerText
    string += string_seven.toString() + ";;";
    var string_six = document.getElementById("id-weight-" + array[x]).innerText
    string_six = string_six.slice(0,string_six.length - 3)
    string += string_six.toString() + ";;";
    var string_eight = document.getElementById("id-typeweight-" + array[x]).innerText
    string += string_eight.toString() + ";;";
    console.log(string);
  }
  string = string.slice(0,string.length - 2)
  var url_string = window.location;
  var url = new URL(url_string);
  var type = url.searchParams.get("type");

  if ( string != ''){
    var pick_up_adress = document.getElementById("id-google-address-b").value
    var client_destination = document.getElementById("id-google-address-d").value
    var params = {
        string: string,
        lat_b: lat_b,
        long_b: long_b,
        lat_d: lat_d,
        long_d: long_d,
        pick_up_adress: pick_up_adress,
        client_destination: client_destination,
        type: type,
    };
    console.log('here');
    var esc = encodeURIComponent;
    var query = Object.keys(params)
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&');

    url = '/quotation_forniture?' + query
    window.location.assign(url)
}
}

function edit(){
  var string = document.getElementById("string").value
  var params = {
      string: string,
      lat_a: lat_a,
      long_a: long_a,
      lat_b: lat_b,
      long_b: long_b,
      lat_c: lat_c,
      long_c: long_c,
      lat_d: lat_d,
      long_d: long_d,
      pick_up_adress: $('#pick_up_adress').val(),
      client_destination: $('#client_destination').val(),
  };

  var esc = encodeURIComponent;
  var query = Object.keys(params)
      .map(k => esc(k) + '=' + esc(params[k]))
      .join('&');

  url = '/map?' + query
  window.location.assign(url)
}
