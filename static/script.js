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

async function checkPlayer(name) {
    const res = await fetch(`http://localhost:8000/check?name=${name}`)

    if (!res.ok) {
        console.error("Error: ", await res.text());
        return;
    }

    const data = await res.json();

    console.log(data);
    return data;
}

document.addEventListener("DOMContentLoaded", () => {
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            checkPlayer(input.value);
            input.value = "";
            startTimer();
        }
    });
})
