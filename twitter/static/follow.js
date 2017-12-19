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