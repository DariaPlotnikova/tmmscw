//Member
$('#addMember').on("click", function () {
    $('#edit-pass').hide();
    $('#hModal').text('Добавить участника');
    $('#addMemSubmit').text('Добавить');
    $('#formNewMem')[0].reset();
    $('#lmFio').siblings().removeClass('active');
    $('#lmGr').siblings().removeClass('active');
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
    $('#edit-pass').show();
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

    var sex = $('#lmSex');
    sex.val(cols[3].innerHTML);

    $('#lmKey').val($(this).siblings()[1].value);
});