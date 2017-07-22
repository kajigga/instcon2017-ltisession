function searchAndRecenter(search) {
    console.log('search', search);
    gc.geocode(search, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });

}

function saveMarker(info) {
    if (info.id == undefined || info.id == '') {
        info.id = marker_id(info);
    }
    var info_to_save = $.extend({}, info, {});
    delete info_to_save.marker;
    marker_db.child(info.id).set(info_to_save);
}

function delete_marker(id, callback) {
    marker_db.child(id).remove(callback);
}


var initMapInstructor = function() {
    $('#instructor_controls').submit(function(e) {
        var search = {
            address: $('#newLocation').val(),
        };
        searchAndRecenter(search);
        e.preventDefault();
    });
    $('#marker_editor').change(function(e) {

        var m_info = all_markers[$('#selected_marker_id').val()];
        m_info.label = $('#selected_marker_label').val();
        m_info.description = $('#selected_marker_description').val();
        m_info.image = $('#selected_marker_image').val();

        saveMarker(m_info);
        prep_m_list();
        e.preventDefault();
    });
    /*$('#marker_editor').submit(function(e){
    // Save the values from the marker editor to Firebase
    console.log('editor submitted');
    var m_info = all_markers[$('#selected_marker_id').val()];
    m_info.label = $('#selected_marker_label').val();
    m_info.description = $('#selected_marker_description').val();
    m_info.image = $('#selected_marker_image').val();

    saveMarker( m_info);
    prep_m_list();
    e.preventDefault();
    });
    */

    map.addListener('click', function(e) {
        var info = {
            order: all_markers.length,
            lat: e.latLng.lat(),
            lng: e.latLng.lng(),
            label: '',
            description: ''
        };

        saveMarker(info)
        //marker_db.push(info);

        var latLng = new google.maps.LatLng(e.latLng.lat(), e.latLng.lng());
        setupMarker(latLng, info)

    });
};

function prep_m_list() {
    $('#marker-list>ul').empty();
    $.each(all_markers, function(idx, mark) {
        var el = $('<li data-id="' + mark.id + '" class="marker-row"><i class="glyphicon glyphicon-trash"></i><i class="glyphicon glyphicon-move"></i> <span class="_label">' + mark.label + '<span></li>');
        $('#marker-list>ul').append(el);
        //el.find('i.glyphicon.glyphicon-trash').click(function(mark.id){ 
        el.find('i.glyphicon.glyphicon-trash').click(function(e) {
            console.log('delete clicked ');
            console.log(mark.id);
            mark.marker.setMap(null);
            delete all_markers[mark.id];
            delete_marker(mark.id, function() {
                prep_m_list();
            });
        });
        el.find('._label, .glyphicon.glyphicon-move').click(function(e) {
            show_info_window(mark);
            setSelectedMarker(mark.marker, mark);
        });
    });
    setListSortable($('#marker-list ul')[0]);
}

function setListSortable(el) {
    // var sortable = Sortable.create(el);
    var sortable = new Sortable(el, {
        // dragging started
        onStart: function( /**Event*/ evt) {
            evt.oldIndex; // element index within parent
        },

        // dragging ended
        onEnd: function( /**Event*/ evt) {
            console.log($(evt.item).data('id'));
            var id = $(evt.item).data('id');

            all_markers[id].order = evt.newIndex;
            saveMarker(all_markers[id]);
            var items = $(evt.target).find('li');
            for (var x = evt.newIndex + 1, l = items.length; x < l; x++) {
                id = $(items[x]).data('id');
                all_markers[id].order = x + 1;
                saveMarker(all_markers[id]);
            }
            //evt.oldIndex; // element's old index within parent
            //evt.newIndex; // element's new index within parent
            //
        },
    });
}
