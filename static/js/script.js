document.addEventListener("DOMContentLoaded", () => {
  const outputContainer = document.getElementById("output-container");

  function runControlScript(scriptName) {
    fetch(`/run_${scriptName}`)
      .then((response) => response.text())
      .then((data) => {
        alert(`${scriptName} has been stopped: ${data}`);
      })
      .catch((error) => {
        console.error(error);
        alert(`Error executing ${scriptName} script.`);
      });
  }

  document.getElementById("face-control-btn").addEventListener("click", () => {
    runControlScript("face_mouse_control");
    alert('You kept your face in front of the camera for 5 seconds!');
  });

  document.getElementById("hand-control-btn").addEventListener("click", () => {
    runControlScript("hand_mouse_control");
    alert('You kept your finger in front of the camera for 5 seconds!');
  });

  document.getElementById("keyboard-control-btn").addEventListener("click", () => {
    runControlScript("keyboard_control");
    alert('You kept your finger in front of the camera for 5 seconds!');
  });

  // Your voice assistant code here
  var voiceAssistantActive = false;

  $("#start-button").click(function() {
    console.log("Start button clicked");
    if (!voiceAssistantActive) {
      voiceAssistantActive = true;
      $(this).prop('disabled', true);
      activateVoiceAssistant();
    }
  });

  function activateVoiceAssistant() {
    $.ajax({
      type: "POST",
      url: "/api/voice-command",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({ "command": "start" }),
      dataType: "json",
      success: function(response) {
        if (response.response === "Voice assistant activated. You can now give voice commands.") {
          // You can add additional handling here if needed
        }
      }
    });
  }
});
