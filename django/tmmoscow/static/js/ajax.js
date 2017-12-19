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

    function success() {
        location.href = "/";
        //location.reload(true);
        // $(this).setTextContent = curRole;
        // $($("a[name='role']").children("b")).detach("b");
    }

    // Поиск команды для подачи заявки
    $('.js-toteam').on('change', function(){
        var form = $('#js-toteam-form');
        form.find('.to-team-message p').addClass('hidden');
        var empty = false;
        $('.js-toteam').each(function(){
            if (!$(this).val()) { empty = true; }
        });
        if (!empty) {
            var url = form.find('#checkTeamUrl').val();
            var data = form.serializeArray();
            $.get(url, data, function(json){
                console.log(json);
                if (json.teams_cnt) {
                    var t = json.teams[0];
                    var text = 'Найдена команда: ' + t.title + ' (' + t.location + '). Руководитель: ' + t.lead + '. Вы можете подать заявку!';
                    form.find('input[name=team]').val(t.id);
                    form.find('.to-team-message p.success').removeClass('hidden');
                    form.find('.to-team-message p.info').removeClass('hidden').text(text);
                    $('.to-team-btn').removeAttr('disabled');
                }
                else {
                    form.find('.to-team-message p.error').removeClass('hidden');
                }
            });
        }
        else {
            form.find('.to-team-message p.error').removeClass('hidden');
        }
    });
});