const input = document.getElementById("inputPlayer");
const timer = document.getElementById("timer");
const scoreboard = document.getElementById("score");
const tryAgain = document.getElementById("tryAgain");
const inputForm = document.getElementById("inputForm");
const guessedList = document.getElementById("guessedList");

const path = window.location.pathname;
const mainTitle = document.getElementById("mainTitle");
const dailyButton = document.getElementById("dailyButton");
const aboutButton = document.getElementById("aboutButton");

const SECONDS = 60;
const guessedPlayers = new Set();
let score = 0;
let interval = null;
let timeRemaining = SECONDS;
let gameEnd = true;

// daily.html
const dailyDate = document.getElementById("dailyDate");
const todaysChallenge = document.getElementById("todaysChallenge");
const monthYearElement = document.getElementById("monthYear");
const datesElement = document.getElementById("dates");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
let calendarDate = new Date();
const today = new Date();

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
    scoreboard.className = '';
    scoreboard.classList.add("score-one");
    
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
    const text = "Players listed: " + score + "\n--------------------------\n" + [...guessedPlayers].map(name => name.toLowerCase()).join("\n") + "\n--------------------------\nhttps://baseball-until-failure.onrender.com";

    navigator.clipboard.writeText(text)
        .then(() => {
            console.log("Copied!");
        })
        .catch(err => {
            console.error("Copy failed:", err);
        });
}

function addPlayerToList(player, teams, positions) {
    const div = document.createElement("div");
    div.classList.add("playerCard");
    div.innerHTML = `<strong>${player.nameFirst} ${player.nameLast}</strong><br>
    ${positions.join(", ")}<br>
    Teams: ${teams.join(", ")}<br>
    Born: ${player.birthYear || "?"}-${player.birthMonth || "?"}-${player.birthDay || "?"}, ${player.birthCity || ""}, ${player.birthState || ""}, ${player.birthCountry || ""} <br>`

    guessedList.prepend(div);
}

function updateScoreStyle() {
    scoreboard.classList.remove("score-one", "score-two", "score-three", "score-four");

    if (score < 3) {
        scoreboard.classList.add("score-one");
    } else if (score < 5) {
        scoreboard.className = '';
        scoreboard.classList.add("score-two");
    } else if (score < 10) {
        scoreboard.className = '';
        scoreboard.classList.add("score-three");
    } else if (score < 20) {
        scoreboard.className = '';
        scoreboard.classList.add("score-four");
    } else if (score < 50) {
        scoreboard.className = '';
        scoreboard.classList.add("score-five");
    } else {
        scoreboard.className = '';
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
            addPlayerToList(data["players"][i], data["teams"][i], data["positions"][i]);
        }
    }

    console.log(data);
    return data;
}

document.addEventListener("DOMContentLoaded", () => {
    restartGame();
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            checkPlayer(input.value);
            input.value = "";
            startTimer();
        }
    });
})

function updateDaily() {
    let date = `${today.toLocaleString("en-US", { month: "long" })} ${today.getDate()}, ${today.getFullYear()}`;
    dailyDate.innerText = date;
}
dailyButton.addEventListener("click", () => {
    window.location.href = "/daily"; 
});

aboutButton.addEventListener("click", () => {
    window.location.href = "/about";
});

mainTitle.addEventListener("click", () => {
    window.location.href = "/";
});

if (path === "/daily") {
    updateDaily();
}
const updateCalendar = () => {
    const currentYear = calendarDate.getFullYear();
    const currentMonth = calendarDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth,0);
    const lastDay = new Date(currentYear, currentMonth +1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();

    const monthYearString = calendarDate.toLocaleString('default', {month: 'long', year: 'numeric'});
    monthYearElement.textContent = monthYearString;

    let datesHTML = '';

    for (let i = firstDayIndex; i > 0; i--) {
        const prevDate = new Date(currentYear, currentMonth, 0 - i+ 1);
        datesHTML += `<div class="date inactive">${prevDate.getDate()}</div>`;
    }

    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass = date.toDateString() === new Date().toDateString() ? 'today' : 'active';
        datesHTML += `<div class = "date ${activeClass}">${i}</div>`;
    }

    for (let i = 1; i <= 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
    }
    datesElement.innerHTML = datesHTML;
}

prevBtn.addEventListener('click', () => {
    calendarDate.setMonth(calendarDate.getMonth() - 1);
    updateCalendar();
})

nextBtn.addEventListener('click', () => {
    calendarDate.setMonth(calendarDate.getMonth() + 1);
    updateCalendar();
})

updateCalendar();