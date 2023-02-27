/**
 * 家族人数変更時の処理
 * 名前項をを人数分用意する
 */
$('#family_number').change(function() {

    // 家族人数
    let family_number = $('#family_number').val();

    let html_text = '';
    let participant_name_html = '<div class="participant-name" > <input type="text" name="name" class="form-control" placeholder="名前" required> </div>';
    
    for(let step = 0; step < family_number; step ++){
        html_text = html_text + participant_name_html.replace('名前', '名前' + (step+1));
    }

    $('.participant-name').html(html_text);

})