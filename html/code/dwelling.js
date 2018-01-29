$.ajax({
    url: Flask.url_for('load_buildings', {'building_id': buildingId}),
    type: 'post',
    data: $('#myForm').serialize(),
    success: function () {
        alert("worked");
    }
});