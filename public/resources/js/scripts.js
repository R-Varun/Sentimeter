navigator.getUserMedia = navigator.getUserMedia ||
navigator.webkitGetUserMedia ||
navigator.mozGetUserMedia;


var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var chunks = [];

var recording = false;
//set up for recording this stuff
//recorder must always have class .record
if (navigator.getUserMedia) {
    console.log('getUserMedia supported.');
    navigator.getUserMedia (
       // constraints - only audio needed for this app
       {
          audio: true
       },
 
       // Success callback
       function(stream) {
        console.log("hell yea");
        var options = {
            mimeType: 'audio/webm',
            audioBitsPerSecond : 256000,
        };
        var mediaRecorder = new MediaRecorder(stream, options);
        
        mediaRecorder.ondataavailable = function(e) {
            chunks.push(e.data);
        }
        $(".record").click(function() {
            if(!recording) {
                mediaRecorder.start();
                console.log(mediaRecorder.state);
                console.log("recorder started");
                $(".record").css("background-color", "red");
                recording= true;

            } else {
                mediaRecorder.stop();                       
                setTimeout( function(){ 
                    var url = "/upload";
                    var form = new FormData();
                    form.append('name', 'test.webm');
                    form.append("audio", new Blob(chunks));           
                    $.ajax({
                        type: "POST",
                        url: url,
                        processData: false,
                        contentType: false,
                        data: form,
                        success: success,
                    });
                    recording = false;
                    console.log(mediaRecorder.state);
                    console.log("recorder stopped");
                    $(".record").css("background-color", "green");                    
                    chunks = [];
                }, 500);     
            }
         });
      
       },
 
       // Error callback
       function(err) {
          console.log('The following gUM error occured: ' + err);
       }
    );
 } else {
    console.log('getUserMedia not supported on your browser!');
 }

function success(data, status, somethingnelse) {
    console.log(data);
    if (data.status == "SUCCESS") {
    window.location = "/session";
    } else {
    console.log("u suck")
    }
}


$(document).ready(function() {
   


});
