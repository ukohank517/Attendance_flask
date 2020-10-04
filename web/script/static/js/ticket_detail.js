function toedit(){
    url = "/ticket/result/edit" + location.search

    window.location.href = url;
}

function update(){    
    var data = {};
    var ticket_memo_list = [];
    var event_id = '';

    // event_id
    var search_params = location.search.substring(1).split('&')
    for(var search_param of search_params){
        var params = search_param.split('=');
        if(params[0] == 'event_id'){
            event_id = params[1];
            console.log(params[1]);
        }
    }    

    for(i = 0; i < $(".member_info").length; i++){
        var ticket_id = $('.ticket_id')[i].textContent;
        var memo = $('.memo')[i].value;
        
        data = {"ticket_id": ticket_id, "memo": memo};
        ticket_memo_list.push(data);
    }
    data = {
        event_id: event_id,
        ticket_memo_list: ticket_memo_list
    };

    $.ajax({
        type:          'post',
        url:           '/ticket/result/update',
        dataType:      'json',
        contentType:   'application/json',
        scriptCharset: 'utf-8',
        data:          JSON.stringify(data),
        success: function(){
            url = "/ticket/result/view" + location.search
            window.location.href = url;
        }, 
        error: function(){
            alert("失敗しました、お手数ですが最初からやり直してください。")
        }
    })


    // document.updateForm.submit();    
}

function create_input_element(name, value){
    var res = document.createElement('input');
    res.setAttribute('type', 'hidden');
    res.setAttribute('name', name);
    res.setAttribute('value', value);

    return res;
}
