$.ajax({
    url: Flask.url_for('load_buildings', {'building_id': buildingId}),
    type: 'post',
    data: $('#myForm').serialize(),
    success: function () {
        alert("worked");
    }
});


$(document).ready(function () {
    $.noty.defaults = {
        layout: 'topRight',
        theme: 'relax',
        type: 'error',
        text: '',

        dismissQueue: false,
        force: true,
        maxVisible: 5,

        template: '<div class="noty_message"><span class="noty_text"></span><div class="noty_close"></div></div>',

        timeout: 10000,
        progressBar: true,

        animation: {
            open: {height: 'toggle'},
            close: {height: 'toggle'},
            easing: 'swing',
            speed: 500
        },
        closeWith: ['click'],

        modal: false,
        killer: true,

        callback: {
            onShow: function () {
            },
            afterShow: function () {
            },
            onClose: function () {
            },
            afterClose: function () {
            },
            onCloseClick: function () {
            }
        },

        buttons: false
    };
});

function saveXml() {
    $.ajax({
        url: Flask.url_for('save_buildings'),
        type: 'post',
        dataType: 'json',
        success: function (response) {
            $('.dropdown-toggle').dropdown('toggle');
        },
        error: function (error) {
            $('.dropdown-toggle').dropdown('toggle');

            noty({
                text: 'Zlyhalo ukladanie XML súboru.'
            });
        }
    });
}

function loadXml() {
    $.ajax({
        url: Flask.url_for('load_buildings'),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            $('.dropdown-toggle').dropdown('toggle');
            replaceBuildingList(response)
        },
        error: function (error) {
            $('.dropdown-toggle').dropdown('toggle');

            noty({
                text: 'Zlyhalo načítavanie XML súboru.'
            });
        }
    });
}

function filterBuildings() {
    $.ajax({
        url: Flask.url_for('filter_buildings'),
        type: 'post',
        dataType: 'html',
        data: $('#filter_form').serialize(),
        success: function (response) {
            replaceBuildingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo filtrovanie budov.'
            });
        }
    });
}

function sortBuildings(sortForm) {
    $.ajax({
        url: Flask.url_for('sort_buildings'),
        type: 'post',
        dataType: 'html',
        data: $(sortForm).serialize(),
        success: function (response) {
            replaceBuildingList(response)
        },
        error: function (error) {
            alert('Zlyhalo triedenie budov.')
        }
    });
}

function addBuilding() {
    $.ajax({
        url: Flask.url_for('add_building'),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replaceBuildingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo pridavanie budovy.'
            });
        }
    });
}

function updateBuilding(buildingForm, buildingId) {
    var streetName = $('#street_' + buildingId)[0].value;
    var streetNumber = $('#number_' + buildingId)[0].value;

    if (!streetName.match(/^\D+$/)) {
        noty({
            text: 'Názov ulice musí byť neprázdny a nesmie obsahovať čísla.'
        });
        return;
    }


    if (streetNumber < 0) {
        noty({
            text: 'Číslo ulice nemože byť záporné.'
        });
        return;
    }

    $.ajax({
        url: Flask.url_for('update_building', {'building_id': buildingId}),
        type: 'post',
        data: $(buildingForm).serialize(),
        error: function (error) {
            noty({
                text: 'Zlyhalo updatovanie budovy.'
            });
        }
    });

}

function deleteBuilding(buildingId) {
    $.ajax({
        url: Flask.url_for('delete_building', {building_id: buildingId}),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replaceBuildingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo mazanie budovy.'
            });
        }
    });
}

function replaceBuildingList(html) {
    var new_building_list = $(html).find('#building_list');
    $('#building_list').replaceWith(new_building_list);
}
