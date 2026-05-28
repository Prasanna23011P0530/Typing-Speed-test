const quotes = [
    "Python is a powerful programming language.",
    "Typing speed improves with daily practice.",
    "Artificial intelligence is changing the world.",
    "Coding becomes easier with consistency.",
    "Success comes from continuous learning."
];

const quoteElement = document.getElementById("quote");
const inputArea = document.getElementById("input-area");

const timerElement = document.getElementById("timer");
const wpmElement = document.getElementById("wpm");
const accuracyElement = document.getElementById("accuracy");
const resultElement = document.getElementById("result");

const startBtn = document.getElementById("start-btn");
const restartBtn = document.getElementById("restart-btn");

let startTime;
let timer;
let currentQuote = "";

function loadQuote(){

    currentQuote =
        quotes[Math.floor(Math.random() * quotes.length)];

    quoteElement.innerText = currentQuote;

    inputArea.value = "";

    resultElement.innerText = "";
}

function startTest(){

    loadQuote();

    inputArea.disabled = false;

    inputArea.focus();

    startTime = new Date().getTime();

    timer = setInterval(updateTimer,1000);
}

function updateTimer(){

    const currentTime = new Date().getTime();

    const seconds =
        Math.floor((currentTime - startTime)/1000);

    timerElement.innerText = seconds + "s";
}

inputArea.addEventListener("input",()=>{

    const typedText = inputArea.value;

    const currentTime = new Date().getTime();

    const timeTaken =
        (currentTime - startTime)/1000;

    const words =
        typedText.trim().split(" ").length;

    const wpm =
        Math.round((words/timeTaken)*60);

    wpmElement.innerText = wpm;

    let correctChars = 0;

    for(let i=0;i<typedText.length;i++){

        if(typedText[i] === currentQuote[i]){
            correctChars++;
        }
    }

    const accuracy =
        Math.round(
            (correctChars/currentQuote.length)*100
        );

    accuracyElement.innerText = accuracy + "%";

    if(typedText === currentQuote){

        clearInterval(timer);

        resultElement.innerText =
            "🔥 Excellent Typing!";
    }

});

restartBtn.addEventListener("click",()=>{

    clearInterval(timer);

    timerElement.innerText = "0s";

    wpmElement.innerText = "0";

    accuracyElement.innerText = "100%";

    inputArea.value = "";

    quoteElement.innerText =
        "Click Start Test to begin...";

    resultElement.innerText = "";

    inputArea.disabled = true;
});

startBtn.addEventListener("click",startTest);