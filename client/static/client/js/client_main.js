function add_1more_element(create_element, placeholder, post_name, item_value, append_to) {
    var item = document.createElement(create_element);
    item.placeholder = placeholder;
    item.className = "form-control m-sm-1";
    item.type = 'text';
    item.name = post_name;
    item.value = item_value;
    document.getElementById(append_to).appendChild(item);
}

// пример JS для страницы "Опыт работы"
function add_exp_form() {
    var count = 1;
    var origin = $("#origin_div").clone();

    $("#add_more").on("click", function () {
        var add = origin.clone();
        var current_div = add.children('div');

        for (var i = 0; i < 6; i++) {
            if (i === 1) {  // 1 select
                var element_select = $(current_div).children('select');
                console.log(element_select);
                var attr_name_s = $(element_select).attr('name');
                console.log(attr_name_s);
                $(element_select).attr('name', attr_name_s + count);
            } else {    // 5 inputs
                var element_input = $(current_div[i]).children('input');
                console.log(element_input);
                var attr_name_i = $(element_input).attr('name');
                console.log(attr_name_i);
                $(element_input).attr('name', attr_name_i + count);
            }
        }
        count++;
        console.log(count);
        add.appendTo("#div_to_add_new");
    });
}
