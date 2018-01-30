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

function addPerson(buildingId, dwellingId, peopleInDwelling) {
    var space = $('#space_' + dwellingId)[0].value;

    if (space === peopleInDwelling) {
        noty({
            text: 'Izba potrebuje viac miesta.'
        });
        return;
    }

    $.ajax({
        url: Flask.url_for('add_person', {building_id: buildingId, dwelling_id: dwellingId}),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replacePeopleList(response);
            replaceInfo(response);
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo pridavanie ubytovaného.'
            });
        }
    });
}

function updatePerson(personForm, buildingId, dwellingId, personId) {
    var name = $('#name_' + personId)[0].value;
    var code = $('#code_' + personId)[0].value;

    if (!name || !code) {
        noty({
            text: 'Osoba musí obsahovať neprázdne meno a kód.'
        });
        return;
    }

    $.ajax({
        url: Flask.url_for('update_person', {building_id: buildingId, dwelling_id: dwellingId, person_id: personId}),
        type: 'post',
        data: $(personForm).serialize(),
        error: function (error) {
            noty({
                text: 'Zlyhalo updatovanie ubytovaného.'
            });
        }
    });

}

function updateDwelling(dwellingForm, buildingId, dwellingId, peopleInDwelling) {
    var space = $('#space_' + dwellingId)[0].value;

    if (space <= 0) {
        noty({
            text: 'Izba musí byť schopná ubytovať aspoň jednu osobu.'
        });
        return;
    }

    if (space < peopleInDwelling) {
        noty({
            text: 'V izbe je viac ľudí, ako navrhnutého priestoru.'
        });
        return;
    }

    $.ajax({
        url: Flask.url_for('update_dwelling', {building_id: buildingId, dwelling_id: dwellingId}),
        type: 'post',
        data: $(dwellingForm).serialize(),
        success: function (response) {
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo updatovanie budovy.'
            });
        }
    });

}

function deletePerson(buildingId, dwellingId, personId) {
    $.ajax({
        url: Flask.url_for('delete_person', {building_id: buildingId, dwelling_id: dwellingId, person_id: personId}),
        type: 'post',
        dataType: 'html',
        success: function (response) {
            replacePeopleList(response);
            replaceInfo(response);
        },
        error: function (error) {
            noty({
                text: 'Zlyhalo mazanie ubytovaného.'
            });
        }
    });
}

function replacePeopleList(html) {
    var newPersonList = $(html).find('#person_list');
    $('#person_list').replaceWith(newPersonList);
}

function replaceInfo(html) {
    var newDwellingInfo = $(html).find('#dwelling_info');
    $('#dwelling_info').replaceWith(newDwellingInfo);
}
