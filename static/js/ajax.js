function nullToCurRole() {
   $.ajax({
       url: '/reg/nullToRole',
       type: 'GET'
   });
}
$(document).ready( function () {
    var b = $("a[name='role']").children("b").text();
    $("a[name='role']").on("click", function () {
        var text = $.trim($(this).text());
        if(text !== b) {
            $.post("/changeRole", {newRole: text}, success);
        }
    });

    function success() {
        location.reload(true);
    }
});