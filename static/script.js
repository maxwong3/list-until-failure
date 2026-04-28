const input = document.getElementById("inputPlayer");
const timer = document.getElementById("timer");
const scoreboard = document.getElementById("score");
const tryAgain = document.getElementById("tryAgain");
const inputForm = document.getElementById("inputForm");
const guessedList = document.getElementById("guessedList");
const SECONDS = 60;
const guessedPlayers = new Set();
let score = 0;
let interval = null;
let timeRemaining = SECONDS;
let gameEnd = true;

function startTimer() {
    if (interval) return;
    interval = setInterval(() => {
        timeRemaining--;

        if (timeRemaining <= 0) {
            clearInterval(interval);
            interval = null;
            timer.innerText = "Out of time!";
            endGame();
        } else {
            timer.innerText = timeRemaining;
        }
    }, 1000)
}

function endGame() {
    if (gameEnd === true) return;
    gameEnd = true;
    const button = document.createElement("button");
    button.innerText = "Try Again";
    button.addEventListener("click", restartGame);
    tryAgain.appendChild(button);
}

function restartGame() {
    timeRemaining = SECONDS;
    score = 0;
    gameEnd = false;

    scoreboard.innerText = 0;
    timer.innerText = SECONDS;
    guessedPlayers.clear();

    if (interval) {
        clearInterval(interval);
        interval = null;
    }

    tryAgain.innerHTML = "";
    input.value = "";
    guessedList.innerHTML = "";
}

function addPlayerToList(player) {
    const div = document.createElement("div");
    div.classList.add("playerCard");
    div.innerHTML = `<strong>${player.nameFirst} ${player.nameLast}</strong><br>
    Born: ${player.birthYear || "?"}-${player.birthMonth || "?"}-${player.birthDay || "?"}, ${player.birthCity || ""}, ${player.birthState || ""}, ${player.birthCountry || ""} <br>
    Debut: ${player.debut || "?"}`

    guessedList.appendChild(div);
}

async function checkPlayer(name) {
    if (gameEnd === true) return;

    const res = await fetch(`/check?name=${name}`)

    if (!res.ok) {
        console.error("Error: ", await res.text());
        return;
    }

    const data = await res.json();
    if (data["count"] >= 1 && !guessedPlayers.has(name.toUpperCase().trim())) {
        guessedPlayers.add(name.toUpperCase().trim());
        timeRemaining += 6;
        score++;
        scoreboard.innerText = score;
        for (let i = 0; i < data["players"].length; i++) {
            addPlayerToList(data["players"][i]);
        }
    }

    console.log(data);
    return data;
}

document.addEventListener("DOMContentLoaded", () => {
    gameEnd = false;
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            checkPlayer(input.value);
            input.value = "";
            startTimer();
        }
    });

})
