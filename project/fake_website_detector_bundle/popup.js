document.getElementById("checkBtn").addEventListener("click", function () {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const url = tabs[0].url;

    fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
      const result = document.getElementById("result");

      if (data.prediction === 1) {
        result.textContent = "Legit Website";
        result.style.color = "green";
      } else {
        result.textContent = "Fake Website Detected!";
        result.style.color = "red";
      }
    })
    .catch(error => {
      console.error("Prediction error:", error);
      const result = document.getElementById("result");
      result.textContent = "Error checking website!";
      result.style.color = "orange";
    });
  });
});
