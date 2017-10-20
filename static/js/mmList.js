$(document).ready(function () {
    $('#qualMemb').val($('#curQual').val());
    $('#surnameMemb').val($('#curSurname').val());
    $('#birthdayMemb').val($('#curBirthday').val());


    Materialize.updateTextFields();
    $('select').material_select();

    var inputToChangePass = $('#toChangePass');

    $('#submitEditMem').click(function () {
        var temp_pass = $('#toChangePass').val();
        // TODO переставить в продакшене на ==
        if(temp_pass.length >= 6){
            $.ajax({
                url: $('#inpt-url-toChangePass').val(),
                type: "POST",
                data: {'pass': temp_pass},
                success: successAjax,
                beforeSend: beforeSendAjax
            });
        }
    });

    function successAjax(response) {
        console.log("Ответ с сервера: " + response);
        $('#preloader').removeClass("active");
        if (response === 'true') {
            inputToChangePass.addClass('valid');
            $('#formSaveEditMember').submit();
        }
        else
            inputToChangePass.addClass('invalid');
    }

    function beforeSendAjax() {
        if (!inputToChangePass.hasClass("invalid"))
            inputToChangePass.addClass('invalid');
        $('#preloader').addClass("active");
    }
});