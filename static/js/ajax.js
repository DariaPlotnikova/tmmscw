function nullToCurRole() {
    $.get($("#inpt-null-role-url").val());
}

$(document).ready(function () {
    var curRole = $("#inpt-change-role-cur").val();
    $(document).on("click", "a[name='role']", function () {
        var newRole = $(this).attr('id');
        if (newRole !== curRole) {
            $.post($("#inpt-change-role-url").val(), {newRole: newRole}, success);
        }
    });

    $('.modal').modal();

    $('#addOrgan').on("click", function () {
        $('#hModal').text('Добавить ркуководителя');
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
        $('#hModal').text('Изменить данные ркуководителя');
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
        $('#olKey').val($(this).siblings()[1].value);
    });

    function success() {
        location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");
    }
});