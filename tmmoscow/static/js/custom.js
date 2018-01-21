$(document).ready(function(){
    // Проход по всем участникам и выставление
    // текста-подсказки для тех, кто не подходит на соревнование
    $('.js-can-apply').each(function(){
        if (!$(this).find('.js-applied').length){
            $(this).empty();
            $(this).text('Не подходит по группам');
        }
    });

    // Проход по всем участникам и выставление
    // текста-подсказки для тех, кто не подходит на дистанцию
    $('.js-day-can-apply').each(function(){
        var dayBlock = $(this).next('.js-day');
        if (!dayBlock.find('.js-applied').length){
            dayBlock.empty();
            dayBlock.text('Не подходит по группам');
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
        if (form.serializeArray().length > 2){
            form.submit();
        }
        else {
            $(this).prev('.error-message').removeClass('hidden');
        }
    });
});