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

    $('#addOrgSubmit').on('click', function () {
        if ($('#olFio').hasClass('valid') && $('#olContact').hasClass('valid')) {
            $('#modalAddOrg').modal('close');
            $('#formNewOrg').submit();
            Materialize.toast('Организатор добален!', 4000);
        } else {
            Materialize.toast('Ошибка при заполнении полей!', 4000);
        }
    });

    function success() {
        location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");
    }
});