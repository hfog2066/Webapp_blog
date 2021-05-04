$('.like-btn').click(function() {
    if ($(this).css('color') == 'rgb(0, 0, 0)') {
        $(this).css('color', 'red')
        var id = $(this).attr('id');
        var url = `/blog/posts/${id}/like`
        $.get(url, function(data) {
            $(`#likesOf${id}`).html(data.likes)
        });
    }
    else {
        $(this).css('color', 'black')
    }
})