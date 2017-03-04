$(document).ready(function(){
    $('.faq-open').on('click', function(){
        $('.faq-text').hide();
        var childText = $(this).find('.faq-text');
        childText.show();
    })
});