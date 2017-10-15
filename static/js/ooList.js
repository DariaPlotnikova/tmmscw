//Organizer
$('#addOrgan').on("click", function () {
    $('#hModal').text('Добавить организатора');
    $('#addOrgSubmit').text('Добавить');
    $('#formNewOrg')[0].reset();
    $('#olFio').siblings().removeClass('active');
    $('#olContact').siblings().removeClass('active');
});

$('#addOrgSubmit').on('click', function () {
    $('ooKey').val("");
    var fio = $('#olFio');
    var cont = $('#olContact');

    if (fio.hasClass('valid') && cont.hasClass('valid')) {
        $('#modalAddOrg').modal('close');
        $('#formNewOrg').submit();

    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});

$('.changeOrg').click(function () {
    $('#hModal').text('Изменить данные организатора');
    $('#addOrgSubmit').text('Изменить');
    var cols = $(this).parent().parent().siblings();
    var fio = $('#olFio');
    fio.val(cols[0].innerHTML);
    fio.siblings().addClass('active');
    fio.addClass('valid');
    var cont = $('#olContact');
    cont.val(cols[1].innerHTML);
    cont.siblings().addClass('active');
    cont.addClass('valid');
    $('#olKey').val($(this).siblings()[2].value);
});