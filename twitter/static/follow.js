    function sendName(elem) {
        var name = $(elem).attr("id");
        var btn_value = $(elem).html();
        data = { username:name };
        if(btn_value == "Follow") {
            $.ajax(
            {
                type: 'POST',
                url: '/fname',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(data),
                success: function(result) {
                    $(elem).html(result)
                }
            });
        }
        else {
            $.ajax(
            {
                type: 'POST',
                url: '/fname',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(data),
                success: function(result) {
                    $(elem).html(result)
                }
            });
        }
    }

    function sendLikes(elem) {
        var tid = $(elem).attr('id');
        data1 = { like:'True', id:tid };
        data2 = { like: 'False', id:tid };
        if($(elem).attr('class') == 'heart') {
            $.ajax(
            {
                type: 'POST',
                url: '/likes',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(data1),
                success: function(result) {
                    $(elem).removeClass('heart');
                    $(elem).addClass('like_color')
                }
            });
        }
        else {
            $.ajax(
            {
                type: 'POST',
                url: '/likes',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(data2),
                success: function(result) {
                    $(elem).removeClass('like_color');
                    $(elem).addClass('heart')
                }
            });
        }
    }