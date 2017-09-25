function nullToCurRole() {
   $.get($("#inpt-null-role-url").val());
}
$(document).ready( function () {
    var curRole = $("#inpt-change-role-cur").val();
    $("a[name='role']").on("click", function () {
        var newRole = $(this).attr('id');
        if(newRole !== curRole) {
            $.post($("#inpt-change-role-url").val(), {newRole: newRole}, success);
        }
    });

    function success() {
        location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");
    }
});