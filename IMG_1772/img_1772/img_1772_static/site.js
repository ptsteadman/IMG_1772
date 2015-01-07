$(document).ready(function(){
    var vid_no = 6;

    $("#add-video button").click(function(){
        console.log("sup");
    });

    $("#load-more").click(function(){
        // do ajax call to append more vids

        var request = $.ajax({
            url: "IMG_1772/videos",
            type: "GET",
            data: { vid_no: vid_no },
            dataType: "html"
        });

        request.done(function(data){
            $("#videos").append(data);
        });
        vid_no += 6;
    });

});
