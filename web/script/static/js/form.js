$(document).ready(function(){
    // 読み込み後に実行する処理
    flatpickr.localize(flatpickr.l10ns.ja);
    flatpickr('#event_date');
  });


// 数字の長さ制限
function sliceMaxLength(elem, maxLength) {
    elem.value = Number(elem.value)
    elem.value = elem.value.slice(0, maxLength);
} 

function enablePublicDate(){
    let event_date_element = $('input[name="event_date"]').val();
    let event_year = event_date_element.slice(0, 4);
    let event_month = event_date_element.slice(5, 7);
    let event_day = event_date_element.slice(8, 10);

    let default_date = new Date(event_year, event_month, event_day);
    default_date.setDate(default_date.getDate() - 7);
    console.log(default_date.getFullYear());
    console.log(default_date.getMonth());
    console.log(default_date.getDate());


    let public_date_element = $('input[name="public_date"]');
    public_date_element.prop('disabled', false);
    flatpickr('#public_date', {
        maxDate: event_date_element,
        dateFormat: "Y-m-d",
        defaultDate: default_date.getFullYear() + "-" + default_date.getMonth() +  "-" + default_date.getDate()
    });
}