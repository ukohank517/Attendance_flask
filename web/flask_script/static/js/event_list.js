function func(event_id){
    var token = prompt("閲覧パスワードを入力してください: ");

    console.log(event_id);
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = '/event/detail';
    
    var input1 = document.createElement('input');
    input1.type = 'hidden';
    input1.name = 'event_id';
    input1.value = event_id;

    var input2 = document.createElement('input');
    input2.type = 'hidden';
    input2.name = 'token';
    input2.value = token;
        
    form.appendChild(input1); form.appendChild(input2);
    form.submit();
}