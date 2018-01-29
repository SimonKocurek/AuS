function updateDwelling(dwellingForm, buildingId, dwellingId) {

    $.ajax({
        url: Flask.url_for('update_dwelling', {'building_id': buildingId, 'dwelling_id': dwellingId}),
        type: 'post',
        data: $(dwellingForm).serialize()
    });

}
