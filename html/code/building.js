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
            replaceDwellingList(response)
        },
        error: function (error) {
            $('.dropdown-toggle').dropdown('toggle');

            noty({
                text: 'Zlyhalo načítavanie XML súboru.'
            });
        }
    });
}

function filterDwellings(buildingId) {
    $.ajax({
        url: Flask.url_for('filter_dwellings', {building_id: buildingId}),
        type: 'post',
        dataType: 'html',
        data: $('#filter_form').serialize(),
        success: function (response) {
            replaceDwellingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo filtrovanie izieb.'
            });
        }
    });
}

function sortDwellings(buildingId, sortForm) {
    $.ajax({
        url: Flask.url_for('sort_dwellings', {building_id: buildingId}),
        type: 'post',
        dataType: 'html',
        data: $(sortForm).serialize(),
        success: function (response) {
            replaceDwellingList(response)
        },
        error: function (error) {
            alert('Zlyhalo triedenie izieb.')
        }
    });
}

function addDwelling(buildingId) {
    $.ajax({
        url: Flask.url_for('add_dwelling', {building_id: buildingId}),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replaceDwellingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo pridavanie izby.'
            });
        }
    });
}

function updateDwelling(dwellingForm, buildingId, dwellingId) {
    var blockId = $('#block_' + dwellingId)[0].value;
    var floorNumber = $('#floor_' + dwellingId)[0].value;
    var cellId = $('#cell_' + dwellingId)[0].value;
    var roomId = $('#room_' + dwellingId)[0].value;

    if (!blockId.match(/[A-Z]/)) {
        noty({
            text: 'Názov bloku musí byť 1 neprázdny veľký znak [A-Z].'
        });
        return;
    }

    if (!cellId.match(/\S+/)) {
        noty({
            text: 'ID bunky musí byť 1 neprázdny znak.'
        });
        return;
    }

    $.ajax({
        url: Flask.url_for('update_dwelling', {'building_id': buildingId, 'dwelling_id': dwellingId}),
        type: 'post',
        data: $(dwellingForm).serialize(),
        error: function (error) {
            noty({
                text: 'Zlyhalo updatovanie budovy.'
            });
        }
    });

}

function deleteDwelling(buildingId, dwellingId) {
    $.ajax({
        url: Flask.url_for('delete_dwelling', {building_id: buildingId, dwelling_id: dwellingId}),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replaceDwellingList(response)
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo mazanie izby.'
            });
        }
    });
}

function replaceDwellingList(html) {
    var newDwellingList = $(html).find('#dwelling_list');
    $('#dwelling_list').replaceWith(newDwellingList);
}
