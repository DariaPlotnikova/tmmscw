//Leader
$('#addLeader').on("click", function () {
    $('#hModal').text('Добавить ркуководителя');
    $('#addLeadSubmit').text('Добавить');
    $('#formNewLead')[0].reset();
    $('#llFio').siblings().removeClass('active');
    $('#llContact').siblings().removeClass('active');
    $('#llTerritory').siblings().removeClass('active');
    $('#llComand').siblings().removeClass('active');
});

$('#addLeadSubmit').on('click', function () {
    $('olKey').val("");
    var fio = $('#llFio');
    var cont = $('#llContact');
    var comm = $('#llComand');
    var terr = $('#llTerritory');

    if (fio.hasClass('valid') && cont.hasClass('valid')
        && comm.hasClass('valid') && terr.hasClass('valid')) {
        $('#modalAddLead').modal('close');
        $('#formNewLead').submit();
    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});

$('.changeLead').click(function () {
    $('#hModal').text('Изменить данные ркуководителя');
    $('#addLeadSubmit').text('Изменить');
    var cols = $(this).parent().parent().siblings();
    var fio = $('#llFio');
    fio.val(cols[0].innerHTML);
    fio.siblings().addClass('active');
    fio.addClass('valid');

    var comm = $('#llComand');
    comm.val(cols[1].innerHTML);
    comm.siblings().addClass('active');
    comm.addClass('valid');

    var terr = $('#llTerritory');
    terr.val(cols[2].innerHTML);
    terr.siblings().addClass('active');
    terr.addClass('valid');

    var cont = $('#llContact');
    cont.val(cols[3].innerHTML);
    cont.siblings().addClass('active');
    cont.addClass('valid');
    $('#llKey').val($(this).siblings()[2].value);
});