$(document).ready(function(){
    $('.text').textillate({
        loop:true,
        sequence: true,
        in: { 
            effect: 'wobble',
        },
        out: { 
            effect: 'wobble',
        }
    })

    // siri config

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 1200,
        height: 100,
        style:"ios",
        amplitude:1,
        speed:"0.12",
        autostart:true,
        frequency:5,
        color:"#000",
      });

    //   siri mssg animation
    
    $('.siri-message').textillate({
        loop:false,
        sequence:true,
        in: { 
            effect: 'fadeInUp',
            sync:true,
        },
        out: { 
            effect: 'fadeOutUp',
            sync:true,
        }
    })

    // mic btn click event

    $("#MicBtn").click(function () { 

        eel.playAssistantSound()

        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });

// Existing function for keyup event
function doc_keyUp(e) {
    // Check for the key "j" and the meta key (Ctrl on Windows, Command on Mac)
    if (e.key === 'j' && e.metaKey) {
        eel.playAssistantSound();  // Play sound through eel (Python integration)
        $("#Oval").attr("hidden", true);  // Hide the Oval element
        $("#SiriWave").attr("hidden", false);  // Show the SiriWave element
        eel.allCommands()();  // Call the eel function for commands
    }
}

// Simulate keyup event after hotword is detected
function trigger_keyup_event() {
    const event = new KeyboardEvent('keyup', {
        key: 'j',
        metaKey: true,  // This is for the MetaKey (or you can change it to ctrlKey for Windows)
        bubbles: true,  // Ensures the event bubbles up through the DOM
        cancelable: true
    });

    // Dispatch the event on the document
    document.dispatchEvent(event);
}

// Expose the function to be called from Python
eel.expose(trigger_keyup_event);

// Start listening for keyup events
document.addEventListener('keyup', doc_keyUp, false);



    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
            

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
            
        }
    });

    




})