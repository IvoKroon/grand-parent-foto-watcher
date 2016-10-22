// using jQuery
//getting the CSRF
$(document).ready(loader());

function loader() {
    //when posting
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //load carousel
    if($("#carousel").length) {
        var slider_speed = $("#slider_speed").val();
        if (slider_speed.length === 0) {
            slider_speed = 3000
        }

        $('.carousel').carousel({
            interval: slider_speed
        })
    }

}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//remove image
$(".remove_image").click(function () {
    var image_id = $(this).parent().parent().children(".image_id").val();
    var image_block = $(this).parent().parent();
    var url = "/images/remove/";

    ajax(url,{image_id:image_id}, "POST").done(function (json) {
        if (json) {
            image_block.remove();
        }
    });
});

//remove image from slider
$(".remove_photo_slider").click(function () {
    var image_id = $(this).parent().children(".image_id").val();
    var image_block = $(this).parent();
    var slider_id = $("#slider_id").val();
    var url = "/slider/ajax/remove/" + slider_id + "/" + image_id;

    ajax(url).done(function (json) {
        if (json) {
            image_block.remove();
        }
    });
});


$("#active_check").click(function () {
    var slider_id = $("#slider_id").val();
    var active = 0;
    var url = "/slider/ajax/change_slider_status/";
    if ($("#active_check").is(":checked")) {
        active = 1;
    }

    ajax(url, {"status": active, "slider_id": slider_id}, "POST").done(function () {
        console.log("DONE");
    })

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
