$(document).ready(function(){
    var vid_no = 6;

    $(".add-video form").submit(function(event){
        return false;
    });

    $(".add-video button").click(function(event){
        $("#person").hide();
        $("#crouch").show();
        $("#crouch").css("display","block");
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
                    data: { vid_no: vid_no + 1, no_vids: 2 },
                    dataType: "html"
                });

                new_vid.done(function(data){
                    $("#person").show();
                    $("#crouch").hide();
                    $("#videos").prepend(data);
                    $("input[name=url]").val("");
                    $("textarea[name=caption]").val("");
                });

                filler_vids.done(function(data){
                    $("#videos").append(data);
                    vid_no = vid_no + 3;
                });
            } else {
                $(".add-video p").text(data.message);
                    $("#person").show();
                    $("#crouch").hide();
            }

        });
    });


    $("#load-more").click(function(){
        // do ajax call to append more vids

        var request = $.ajax({
            url: "IMG_1772/videos",
            type: "GET",
            data: { vid_no: vid_no, no_vids: 3 },
            dataType: "html"
        });

        request.done(function(data){
            $("#videos").append(data);
        });
        vid_no += 6;
    });

    $(".player-wrapper").hover(function(){
        console.log("hey");
        $(this).css("-webkit-filter","none");
    });
    
    $(".player-wrapper").on("touchstart",function(){
        console.log("hey");
        $(this).css("-webkit-filter","none");
    });

});
