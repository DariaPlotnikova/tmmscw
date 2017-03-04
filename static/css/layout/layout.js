$(document).ready(function(){
    $('.faq-open').on('click', function(e){
        e.preventDefault();
        $('.faq-text').hide().animate(150);
        var childText = $(this).find('.faq-text');
        childText.slideDown(200);
        $('.faq-open').attr('style', '');
        $(this).attr('style', 'border-left: 20px solid #E94141;');
    })
});