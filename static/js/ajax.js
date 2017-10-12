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

    function success() {
        location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");
    }
});