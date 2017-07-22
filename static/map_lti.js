// Remember to change this url to your own if you use this.
var config = {
  apiKey: "AIzaSyDRTJg6neESg3jF27JNI1u3jVtGvBR3sO8",
  authDomain: "instcon2017.firebaseapp.com",
  databaseURL: "https://instcon2017.firebaseio.com",
  projectId: "instcon2017",
  storageBucket: "",
  messagingSenderId: "869396139163"
};
firebase.initializeApp(config);
firebase.auth().signInAnonymously().catch(function(error) {
    // Handle Errors here.
    //   var errorCode = error.code;
    //     var errorMessage = error.message;
    //       // ...
    //       });
})

var rootRef = firebase.database().ref();

//var firebase = new Firebase('https://burning-fire-7264.firebaseio.com/'); //#-KGMjngqOsfdYmQVAuOQ|84de6e0176b2809975487d2c428c4965');
//var marker_db = firebase.child('markers:'+LTI_ENV.context_id);
var marker_db = rootRef.child('markers:'+LTI_ENV.context_id);
var map;
var gc = new google.maps.Geocoder();
var infowindow;
var all_markers = {};

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
  zoom: 8,
  center: {lat: 39.57605638518604, lng: -105.9521484375}, // Keystone, Colorado
  zoomControl: true,
  mapTypeControl: false,
  scaleControl: false,
  streetViewControl: false,
  rotateControl: false,
  fullscreenControl: false
  });
  
  infowindow = new google.maps.InfoWindow();
  google.maps.event.addListener(infowindow, 'domready', function() {
    
    // Reference to the DIV which receives the contents of the infowindow using jQuery
    var iwOuter = $('.gm-style-iw');
    
    /* The DIV we want to change is above the .gm-style-iw DIV.
    * So, we use jQuery and create a iwBackground variable,
    * and took advantage of the existing reference to .gm-style-iw for the previous DIV with .prev().
    */
    var iwBackground = iwOuter.prev();
    
    // Remove the background shadow DIV
    iwBackground.children(':nth-child(2)').css({'display' : 'none'});
    
    // Remove the white background DIV
    iwBackground.children(':nth-child(4)').css({'display' : 'none'});
    
    var iwCloseBtn = iwOuter.next();
    
    // Apply the desired effect to the close button
    iwCloseBtn.css({
    opacity: '1', // by default the close button has an opacity of 0.7
    right: '9px', top: '-4px', // button repositioning
    border: '7px solid #48b5e9', // increasing button border and new color
    'width': '40px',
    'height': '40px',
    'background-color': '#fff',
    'border-radius': '20px', // circular effect
    'box-shadow': '0 0 5px #3990B9' // 3D effect to highlight the button
    });
    iwCloseBtn.find('img').css({
    left: '5px',
    top: '-328px'
    });
    
    
    // The API automatically applies 0.7 opacity to the button after the mouseout event.
    // This function reverses this event to the desired value.
    iwCloseBtn.mouseout(function(){
      $(this).css({opacity: '1'});
    });
    
  });
}

marker_db.orderByChild("order").on("child_added", function(snapshot, prevChildKey) {
 // Get latitude and longitude from Firebase.
 var newPosition = snapshot.val();

 // Create a google.maps.LatLng object for the position of the marker.
 // A LatLng object literal (as above) could be used, but the heatmap
 // in the next step requires a google.maps.LatLng object.
 var latLng = new google.maps.LatLng(newPosition.lat, newPosition.lng);
 setupMarker(latLng, newPosition);
});

function marker_id(info){
 return LTI_ENV.custom_canvas_user_id +'::'+LTI_ENV.context_id+'::'+
 info.lat.toString().replace('.','')+
 '::'+info.lng.toString().replace('.','')
}

function setupMarker(latLng, info){
 if(info.id == undefined || info.id == ''){
 info.id = marker_id(info) ;
 }

 // Place a marker at that location.
 var draggable = LTI_ENV.is_instructor;
 var marker = new google.maps.Marker({
 position: latLng,
 map: map,
 title:' some title ',
 draggable: draggable
 });

 info.marker = marker;
 all_markers[info.id] = info;
 // Add a click handler to the marker so it shows the info window when...clicked
 marker.addListener('click', function(){
 show_info_window( info );
 setSelectedMarker(marker, all_markers[info.id]);
 });
 if(LTI_ENV.is_instructor){
 marker.addListener('dragend', function(e){

 var m_info = all_markers[info.id];
 m_info.lat = e.latLng.lat();
 m_info.lng = e.latLng.lng();
 saveMarker( m_info);
 });
 }

 $('#marker-list>ul li').remove();
 if(prep_m_list){ prep_m_list(); };
}

function setSelectedMarker( marker, info){
 $('#selected_marker_id').val(info.id); 
 $('#selected_marker_label').val(info.label); 
 $('#selected_marker_description').val(info.description); 
 $('#selected_marker_image').val(info.image); 
 selected_marker = {marker:marker, info: info};
};

function show_info_window( info ){
 var img_src = (all_markers[info.id].image) ? '<img src="'+ all_markers[info.id].image+'" width="100px" />' : '' ;
 var content = '<div id="iw-container" data-info-id="'+all_markers[info.id].id+'"> ' +
 '<div class="iw-title">'+ all_markers[info.id].label +'</div>' +
 '<div class="iw-content">' +
 '<div class="iw-subTitle">subtitle</div>' +
 img_src+
 '<p class="marker_description">'+ all_markers[info.id].description +'</p>' +
 '</div>' +
 '<div class="iw-bottom-gradient"></div>' +
 '</div>';

 infowindow.setContent(content);
 infowindow.open(map, info.marker); 
};

