function nullToCurRole() {
   $.get($("#inpt-null-role").val());
}
$(document).ready( function () {
    var curRole = $("a[name='role']").children("b").text();
    $("a[name='role']").on("click", function () {
        var newRole = $.trim($(this).text());
        if(newRole !== curRole) {
            $.post($("#inpt-change-role").val(), {newRole: newRole}, success);
        }
    });

    function success() {
        location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");

    }
});