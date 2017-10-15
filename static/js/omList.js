//Member
$('#addMember').on("click", function () {
    $('#hModal').text('Добавить участника');
    $('#addMemSubmit').text('Добавить');
    $('#formNewMem')[0].reset();
    $('#omFio').siblings().removeClass('active');
    $('#omGr').siblings().removeClass('active');
    $('#omRazr').val("б/р");
    $('select').material_select();
});

$('#addMemSubmit').on('click', function () {
    var fio = $('#omFio');
    var gr = $('#omGr');
    // TODO сделать проверку года рожления
    // if(int(gr.val() < 1900 && gr.val() > 2030){
    //     gr.addClass('invalid');
    // } else {
    //     gr.removeClass('invalid');
    //     gr.addClass('valid');
    // }

    if (fio.hasClass('valid') && gr.hasClass('valid')) {
        $('#modalAddMem').modal('close');
        $('#formNewMem').submit();
    } else {
        Materialize.toast('Ошибка при заполнении полей!', 4000);
    }
});

$('.changeMem').click(function () {
    $('omKey').val("");
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

    var comm = $('#omComand');
    var tempString = cols[3].innerHTML + ' (' + cols[4].innerHTML + ')';
    alert(tempString);
    comm.val(tempString);
    $('select').material_select();
    //comm.val(cols[3].innerHTML + ' (' + cols[4].innerHTML + ')');
    // var comm = String(cols[3].innerHTML + ' (' + cols[4].innerHTML + ')');
    // $('li:text("'+comm+'")').addClass('active selected');

    $('#omKey').val($(this).siblings()[2].value);
});