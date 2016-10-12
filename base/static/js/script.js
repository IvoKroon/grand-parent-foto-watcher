// using jQuery
//getting the CSRF
$(document).ready(loader());

function loader() {
    //when posting
    var csrftoken = getCookie('csrftoken');
}

function remove_image_from_slider() {
    ajax("http://127.0.0.1:8001/slider/ajax/remove/8/23");
}
$(".remove_photo").click(function () {
    //image id
    var image_id = $( this ).parent().children(".image_id").val();
    var image_block = $(this).parent();
    var slider_id = $("#slider_id").val();
    var url = "http://127.0.0.1:8001/slider/ajax/remove/"+slider_id+"/"+image_id;
    ajax(url).done(function (json) {
            if(json){
                image_block.remove();
            }
        });
});

function ajax(url, data, type) {
    type = typeof type !== 'undefined' ? type : "GET";

    return $.ajax({
        url: url,
        type: type,
        dataType: 'json',
        data: data,
        //success
        success: function (json) {
            return true;
        },
        //error handeling
        error: function (xhr) {
            console.log(xhr.status + ": " + xhr.responseText);
            return false;
        }
    });
}

//Do ajax
// function ajax(url, data, type) {
//     // default
//
//     //ajax function
//     $.ajax({
//         url: url,
//         type: type,
//         dataType: 'json',
//         data: data,
//         //success
//         success: function (json) {
//             console.log(json);
//             return true;
//         },
//         //error handeling
//         error: function (xhr) {
//             console.log(xhr.status + ": " + xhr.responseText);
//             return false;
//         }
//     });
// }

function show(json){
    console.log("wow "+ json)
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
