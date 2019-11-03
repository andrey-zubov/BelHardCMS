let objDiv = document.getElementById("messages");
let chats = $('.chat_block');
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

                            let new_mes ='<div class="message_block_left"><div class="reply-body">' +
                                '<div class="list-inline" id="' + data[dat].message_id + '"><div class="name_field">'
                                + data[dat].author_first_name + ' ' +  data[dat].author_last_name +'</div><div class="message_field">'
                                + data[dat].message + '</div></div><div class="date_field"><small>'
                                + data[dat].pub_date + '</small></div></div></div>';
                            if (data[dat].author_id === data[dat].user_id ){
                               new_mes ='<div class="message_block_right"><div class="reply-body">' +
                                    '<div class="list-inline" id="' + data[dat].message_id + '"><div class="name_field">'
                                    + data[dat].author_first_name + ' ' +  data[dat].author_last_name +'</div><div class="message_field">'
                                    + data[dat].message + '</div></div><div class="date_field"><small>'
                                    + data[dat].pub_date + '</small></div></div></div>'
                            }

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
                        new_mes ='<div class="message_block_left"><div class="reply-body">' +
                                '<div class="list-inline" id="' + data[dat].message_id + '"><div class="name_field">'
                                + data[dat].author_first_name + ' ' +  data[dat].author_last_name +'</div><div class="message_field">'
                                + data[dat].message + '</div></div><div class="date_field"><small>'
                                + data[dat].pub_date + '</small></div></div></div>';
                            if (data[dat].author_id === data[dat].user_id){
                               new_mes ='<div class="message_block_right"><div class="reply-body">' +
                                    '<div class="list-inline" id="' + data[dat].message_id + '"><div class="name_field">'
                                    + data[dat].author_first_name + ' ' +  data[dat].author_last_name +'</div><div class="message_field">'
                                    + data[dat].message + '</div></div><div class="date_field"><small>'
                                    + data[dat].pub_date + '</small></div></div></div>'
                            }

                        $("#innerMessages").append(new_mes) ;
                        objDiv.scrollTop = objDiv.scrollHeight;

                    }
                    chats.css("background",'#007e7e');
                    $(Element).css("background",'#1bffdf');
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
                    new_mes ='<div class="message_block_left"><div class="reply-body">' +
                                '<div class="list-inline" id="' + data.message_id + '"><div class="name_field">'
                                + data.author_first_name + ' ' +  data.author_last_name +'</div><div class="message_field">'
                                + data.message + '</div></div><div class="date_field"><small>'
                                + data.pub_date + '</small></div></div></div>';
                            if (data.author_id === data.user_id){
                               new_mes ='<div class="message_block_right"><div class="reply-body">' +
                                    '<div class="list-inline" id="' + data.message_id + '"><div class="name_field">'
                                    + data.author_first_name + ' ' +  data.author_last_name +'</div><div class="message_field">'
                                    + data.message + '</div></div><div class="date_field"><small>'
                                    + data.pub_date + '</small></div></div></div>'
                            }

                    $("#innerMessages").append(new_mes);
                    objDiv.scrollTop = objDiv.scrollHeight;
                }
            })
        }

    }