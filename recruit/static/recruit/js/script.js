let objDiv = document.getElementById("messages");
    let chat_id;
    $('document').ready(function () {
        $.ajax({
                'url': '/recruit/check_mes/',
                success: function (data) {
                    for (c in data){
                        if (data[c].count != 0) {
                            document.getElementById('count_'+ data[c].chat_id).hidden = false;
                            document.getElementById('count_'+ data[c].chat_id).innerHTML =  data[c].count;
                        }
                        else {
                            document.getElementById('count_'+ data[c].chat_id).hidden = true;
                        }
                    }
                }
            });

        setInterval(function(){
            if (chat_id && $('ul.list-inline').last().attr('id')){
                var last_id = $('ul.list-inline').last().attr('id');
                $.ajax({
                    'url': '/recruit/chat_update/',
                    'data': {'chat_id': chat_id, 'last_id': last_id},
                    success: function (data) {
                        for (let dat in data){

                            let new_mes = '<div class="list-group-item "><div class="reply-body"><ul class="list-inline" id=' + data[dat].message_id+
                                   '><li class="drop-left-padding"><strong class="list-group-item-heading">' + data[dat].author_name +
                                    '</strong></li><li class="pull-right text-muted"><small>' + data[dat].pub_date +
                                    '</small></li></ul><div>' + data[dat].message + '</div></div></div>';

                            $("#innerMessages").append(new_mes) ;
                            objDiv.scrollTop = objDiv.scrollHeight;
                        }

                    }
                })
            }


        }, 5000);

        setInterval(function(){
            $.ajax({
                'url': '/recruit/check_mes/',
                success: function (data) {
                    for (c in data){
                        if (data[c].count != 0) {
                            document.getElementById('count_'+ data[c].chat_id).hidden = false;
                            document.getElementById('count_'+ data[c].chat_id).innerHTML =  data[c].count;
                        }
                        else {
                            document.getElementById('count_'+ data[c].chat_id).hidden = true;
                        }
                    }
                }
            });
        }, 5000);

    });

    function show_messages(Element) {
        chat_id = Element.id;
        $.ajax({
                'url': '/recruit/get_messages/',
                'data': {'chat_id' : Element.id},
                success: function (data) {
                    $("#innerMessages").html("");
                    for (let dat in data){
                        let new_mes = '<div class="list-group-item "><div class="reply-body"><ul class="list-inline" id=' + data[dat].message_id+
                               '><li class="drop-left-padding"><strong class="list-group-item-heading">' + data[dat].author_name +
                                '</strong></li><li class="pull-right text-muted"><small>' + data[dat].pub_date +
                                '</small></li></ul><div>' + data[dat].message + '</div></div></div>';

                        $("#innerMessages").append(new_mes) ;
                        objDiv.scrollTop = objDiv.scrollHeight;
                    }
                }
        })
    }

    function send_message() {
        if (chat_id && document.getElementById('textField').value) {
            $.ajax({
                'url': '/recruit/send_message/',
                'data': {'chat_id': chat_id, 'message': document.getElementById('textField').value},
                success: function (data) {
                    document.getElementById("textField").value = "";
                    let new_mes = '<div class="list-group-item "><div class="reply-body"><ul class="list-inline" id=' + data.message_id +
                        '><li class="drop-left-padding"><strong class="list-group-item-heading">' + data.author_name +
                        '</strong></li><li class="pull-right text-muted"><small>' + data.pub_date +
                        '</small></li></ul><div>' + data.message + '</div></div></div>';

                    $("#innerMessages").append(new_mes);
                    objDiv.scrollTop = objDiv.scrollHeight;
                }
            })
        }

    }