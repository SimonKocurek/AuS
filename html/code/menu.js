function saveBuildings() {
    $.ajax({
        url: Flask.url_for('save_buildings'),
        type: 'post'
    });
}

function updateBuilding(buildingForm, buildingId) {

    $.ajax({
        url: Flask.url_for('update_building', {'building_id': buildingId}),
        type: 'post',
        data: $(buildingForm).serialize()
    });

}
