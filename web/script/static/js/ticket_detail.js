function toedit(){
    url = "/ticket/result/edit" + location.search

    window.location.href = url;
}

function update(){
    var data = {};
    var ticket_memo_list = [];
    for(i = 0; i < $(".member_info").length; i++){
        var ticket_id = $('.ticket_id')[i].textContent;
        var memo = $('.memo')[i].value;
        
        data = {"ticket_id": ticket_id, "memo": memo};
        ticket_memo_list.push(data);
    }
    data = {ticket_memo_list: ticket_memo_list};

    $.ajax({
      type:          'post',
      url:           '/api/ticket/result/update',
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
