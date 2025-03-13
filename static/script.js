document.getElementById("record-btn").addEventListener("click", async () => {
    let statusText = document.getElementById("status");
    statusText.innerText = "Recording...";

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    let chunks = [];

    mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
    mediaRecorder.onstop = async () => {
        statusText.innerText = "Processing...";

        // Convert recorded chunks into a blob
        const audioBlob = new Blob(chunks, { type: "audio/wav" });
        let formData = new FormData();
        formData.append("audio", audioBlob, "recorded_audio.wav");

        // Upload to Flask server
        let response = await fetch("/upload", { method: "POST", body: formData });
        let result = await response.json();
        
        // Display feedback
        document.getElementById("feedback").innerText = `Energy: ${result.energy}, Pitch: ${result.pitch_variability}, Suggestion: ${result.suggestion}`;
        statusText.innerText = "Recording complete. See feedback below.";
    };

    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), 10000); // Stop after 10 seconds
});
