const input = document.getElementById("inputPlayer");
const timer = document.getElementById("timer");
const SECONDS = 60;
let startTime = 0;
let interval = null;

function startTimer() {
    if (interval) return;
    startTime = Date.now();
    interval = setInterval(() => {
        let timeElapsed = Math.floor((Date.now() - startTime) / 1000);
        let timeRemaining = SECONDS - timeElapsed;

        if (timeRemaining <= 0) {
            clearInterval(interval);
            interval = null;
            timer.innerText = "Out of time!";
        } else {
            timer.innerText = timeRemaining;
        }
    }, 1000)
}

document.addEventListener("DOMContentLoaded", () => {
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            console.log("Text entered:", input.value);
            input.value = "";
            startTimer();
        }
    });
})