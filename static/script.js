const input = document.getElementById("inputPlayer");
const timer = document.getElementById("timer");
const scoreboard = document.getElementById("score");
const tryAgain = document.getElementById("tryAgain");
const inputForm = document.getElementById("inputForm");
const guessedList = document.getElementById("guessedList");

const mainTitle = document.getElementById("mainTitle");
const dailyButton = document.getElementById("dailyButton");
const aboutButton = document.getElementById("aboutButton");

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
    const copyButton = document.createElement("button");
    button.innerText = "Try Again";
    button.addEventListener("click", restartGame);
    copyButton.innerText = "Copy Results";
    copyButton.addEventListener("click", copyResults);
    tryAgain.appendChild(button);
    tryAgain.appendChild(copyButton);
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
function copyResults() {
    const text = "Players listed: " + score + "\n--------------------------\n" + [...guessedPlayers].join("\n") + "\n--------------------------\nhttps://baseball-until-failure.onrender.com";

    navigator.clipboard.writeText(text)
        .then(() => {
            console.log("Copied!");
        })
        .catch(err => {
            console.error("Copy failed:", err);
        });
}

function addPlayerToList(player) {
    const div = document.createElement("div");
    div.classList.add("playerCard");
    div.innerHTML = `<strong>${player.nameFirst} ${player.nameLast}</strong><br>
    Born: ${player.birthYear || "?"}-${player.birthMonth || "?"}-${player.birthDay || "?"}, ${player.birthCity || ""}, ${player.birthState || ""}, ${player.birthCountry || ""} <br>
    Debut: ${player.debut || "?"}`

    guessedList.prepend(div);
}

function updateScoreStyle() {
    scoreboard.classList.remove("score-one", "score-two", "score-three", "score-four");

    if (score < 3) {
        scoreboard.classList.add("score-one");
    } else if (score < 5) {
        scoreboard.classList.add("score-two");
    } else if (score < 10) {
        scoreboard.classList.add("score-three");
    } else if (score < 20) {
        scoreboard.classList.add("score-four");
    } else if (score < 50) {
        scoreboard.classList.add("score-five");
    } else {
        scoreboard.classList.add("score-six");
    }
}

function replaceChars(str, charMap) {
  return [...str]
    .map(c => charMap[c] || c)
    .join('');
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
        updateScoreStyle();
        for (let i = 0; i < data["players"].length; i++) {
            addPlayerToList(data["players"][i]);
        }
    }

    console.log(data);
    return data;
}

document.addEventListener("DOMContentLoaded", () => {
    restartGame();
    scoreboard.classList.add("score-one");
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            checkPlayer(input.value);
            input.value = "";
            startTimer();
        }
    });
})

dailyButton.addEventListener("click", () => {
    window.location.href = "/daily"; 
});

aboutButton.addEventListener("click", () => {
    window.location.href = "/about";
});

mainTitle.addEventListener("click", () => {
    window.location.href = "/";
});