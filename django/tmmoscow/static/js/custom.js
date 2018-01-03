$(document).ready(function(){
    $('.js-can-apply').each(function(){
        console.log($(this).find('label').length);
        if (!$(this).find('label').length){
            $(this).empty();
            $(this).text('Не подходит по группам');
        }
    });

    // Заявить участников на соревнования (шаг 1)
    $('.js-to-competition').on('click', function(){
        $(this).closest('p.error-message').addClass('hidden');
        var form = $('#addToCompetitionForm');
        if (form.serializeArray().length){
            form.submit();
        }
        else {
            $(this).prev('.error-message').removeClass('hidden');
        }
    });

    // Заявить участников на дистанции (шаг 2)
    $('.js-to-distances').on('click', function(){
        $(this).closest('p.error-message').addClass('hidden');
        var form = $('#addToDistsForm');
        if (form.serializeArray().length > 1){
            form.submit();
        }
        else {
            $(this).prev('.error-message').removeClass('hidden');
        }
    });
});