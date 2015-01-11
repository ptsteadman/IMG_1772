$(document).ready(function(){
    var app = {}
    app.vid_no = 6;

    function addEventListeners(){
        $(".player-wrapper").hover(function(){
            $(this).css("-webkit-filter","none");
            $(this).css("filter","none");
            $(this).css("-moz-filter","none");
        });

        var isTouchDevice = 'ontouchstart' in document.documentElement;
        if(isTouchDevice){
            $(".player-wrapper").css("-webkit-filter","none");
            $(".player-wrapper").css("filter","none");
            $(".player-wrapper").css("-moz-filter","none");

        }

    }
    
    addEventListeners();

    $(".add-video form").submit(function(event){
        return false;
    });

    $(".add-video button[type=submit]").click(function(event){
        $(".preview-player").hide();
        $(".preview-buttons").hide();
        $(".person").hide();
        $(".crouch").show();
        $(".crouch").css("display","block");
        event.preventDefault();
        var request = $.ajax({
            url: "IMG_1772/videos",
            type: "POST",
            data: {
                url : $("input[name=url]").val(),
                caption: $("textarea[name=caption]").val()
            },
            dataType: "json"
        });

        request.done(function(data){
            if (data.success){
                $(".add-video p").text(data.message);
                var new_vid = $.ajax({
                    url: "IMG_1772/videos",
                    type: "GET",
                    data: { vid_no: 0, no_vids: 1 },
                    dataType: "html"
                });


                var filler_vids = $.ajax({
                    url: "IMG_1772/videos",
                    type: "GET",
                    data: { vid_no: app.vid_no + 1, no_vids: 2 },
                    dataType: "html"
                });

                new_vid.done(function(data){
                    $(".person").show();
                    $(".crouch").hide();
                    $("#videos").prepend(data);
                    $("input[name=url]").val("");
                    $("textarea[name=caption]").val("");
                });

                filler_vids.done(function(data){
                    $("#videos").append(data);
                    vid_no = app.vid_no + 3;
                    addEventListeners();
                });
            } else {
                $(".add-video p").text(data.message);
                    $(".person").show();
                    $(".crouch").hide();
            }

        });
    });


    $("#load-more").click(function(){
        var request = $.ajax({
            url: "IMG_1772/videos",
            type: "GET",
            data: { vid_no: app.vid_no, no_vids: 3 },
            dataType: "html"
        });

        request.done(function(data){
            $("#videos").append(data);
            addEventListeners();
        });
        app.vid_no += 6;
    });
    
    // random video button

    $(".person").click(function(){
        $(".person").hide(); $(".crouch").show();
        $(".crouch").css("display","block");
        
        $.ajax({
            type: "GET",
            url: "IMG_1772/random",
            success: function(data){
                $(".crouch").hide();
                $(".preview-buttons").show();
                var vid = data['vid']
                app.src = "http://www.youtube.com/embed/" + vid 
                var options = "?controls=0&showinfo=0&modestbranding=1i&cc_load_policy=1"
                var player = "<iframe class='player' src='" + app.src + options + "' frameborder='0' allowfullscreen></iframe>"
                $(".preview-player").html(player);
            }
        });
    });

    $(".another").click(function(){
        $.ajax({
            type: "GET",
            url: "IMG_1772/random",
            success: function(data){
                $(".crouch").hide();
                $(".preview-buttons").show();
                var vid = data['vid']
                app.src = "http://www.youtube.com/embed/" + vid 
                var options = "?controls=0&showinfo=0&modestbranding=1i&cc_load_policy=1"
                var player = "<iframe class='player' src='" + app.src + options + "' frameborder='0' allowfullscreen></iframe>"
                $(".preview-player").html(player);
            }
        });
    });

    $(".share").click(function(){
        $("input[name=url]").val(app.src);
        $("textarea[name=caption]").focus();
    });

    
});
