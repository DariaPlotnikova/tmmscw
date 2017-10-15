//Member
$('#addMember').on("click", function () {
    $('#lmKey').val("");
    $('#hModal').text('Добавить участника');
    $('#addMemSubmit').text('Добавить');
    $('#formNewMem')[0].reset();
    $('#lmFio').siblings().removeClass('active');
    $('#lmGr').siblings().removeClass('active');
    $('#lmRazr').val("б/р");
    $('select').material_select();
    $('#pass-to-edit-input').val("");
    $('#passToEdit').val("");
    $.ajax({
        url: $('#inpt-url-edit-pass').val(),
        type: "GET",
        async: false,
        cache: false,
        success: function (value) {
            $('#pass-to-edit-input').val(value);
            $('#passToEdit').val(value);
        }
    });
});

$('#addMemSubmit').on('click', function () {
    var fio = $('#lmFio');
    var gr = $('#lmGr');

    if (fio.hasClass('valid') && gr.hasClass('valid') && gr.val() > 1930 && gr.val() < 2030) {
        $('#modalAddMem').modal('close');
        $('#formNewMem').submit();
    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});

$('.changeMem').click(function () {
    $('lmKey').val("");
    $('#hModal').text('Изменить данные участника');
    $('#addMemSubmit').text('Изменить');

    var cols = $(this).parent().parent().siblings();
    var fio = $('#lmFio');
    fio.val(cols[0].innerHTML);
    fio.siblings().addClass('active');
    fio.addClass('valid');

    var gr = $('#lmGr');
    gr.val(cols[1].innerHTML);
    gr.siblings().addClass('active');
    gr.addClass('valid');

    var qual = $('#lmRazr');
    qual.val(cols[2].innerHTML);
    $('select').material_select();

    var sex = $('#lmSex');
    sex.val(cols[3].innerHTML);

    $('#pass-to-edit-input').val($(this).siblings()[2].value);
    $('#passToEdit').val($(this).siblings()[2].value);

    $('#lmKey').val($(this).siblings()[1].value);
});

$("#changeCommSubmit").click(function () {
    var terr = $('#terryTeam');
    var commName = $('#nameTeam');

    if(terr.hasClass('valid') && commName.hasClass('valid')) {
        $('#modalChangeComm').modal('close');
        $('#formSaveTeam').submit();
    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});