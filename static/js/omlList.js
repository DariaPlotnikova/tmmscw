//Organizer
$('#addOrgan').on("click", function () {
    $('#hModal').text('Добавить организатора');
    $('#addOrgSubmit').text('Добавить');
    $('#formNewOrg')[0].reset();
    $('#olFio').siblings().removeClass('active');
    $('#olContact').siblings().removeClass('active');
});

$('#addOrgSubmit').on('click', function () {
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

//Member
$('#addMember').on("click", function () {
    $('#hModal').text('Добавить участника');
    $('#addMemSubmit').text('Добавить');
    $('#formNewMem')[0].reset();
    $('#omFio').siblings().removeClass('active');
    $('#omContact').siblings().removeClass('active');
    $('#omTerritory').siblings().removeClass('active');
    $('#omComand').siblings().removeClass('active');
});

$('#addMemSubmit').on('click', function () {
    var fio = $('#omFio');
    var gr = $('#omGr');

    if (fio.hasClass('valid') && gr.hasClass('valid')) {
        $('#modalAddMem').modal('close');
        $('#formNewMem').submit();
    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});

$('.changeMem').click(function () {
    $('#hModal').text('Изменить данные участника');
    $('#addMemSubmit').text('Изменить');

    var cols = $(this).parent().parent().siblings();
    var fio = $('#omFio');
    fio.val(cols[0].innerHTML);
    fio.siblings().addClass('active');
    fio.addClass('valid');

    var gr = $('#omGr');
    gr.val(cols[1].innerHTML);
    gr.siblings().addClass('active');
    gr.addClass('valid');

    var qual = $('#omRazr');
    qual.val(cols[2].innerHTML);
    qual.siblings().addClass('active');
    qual.addClass('valid');

    var comm = $('#omComand');
    comm.val(cols[3].innerHTML);
    comm.siblings().addClass('active');
    comm.addClass('valid');

    var terr = $('#omTerritory');
    terr.val(cols[4].innerHTML);
    terr.siblings().addClass('active');
    terr.addClass('valid');

    alert($(this).siblings()[2].value);
    $('#omKey').val($(this).siblings()[2].value);
});

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