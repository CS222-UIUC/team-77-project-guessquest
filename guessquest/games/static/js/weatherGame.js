const test = [
  { question: "What is the weather in Urbana?", answer: "50" },
  { question: "What is the weather in Spain?", answer: "37" },
  { question: "What is the weather in Australia?", answer: "79" },
  { question: "What is the weather in Japan?", answer: "55" },
  { question: "What is the weather in Brazil?", answer: "70" },
];

const questionAsked = document.getElementById("question");
const answerText = document.getElementById("answer");

let questionNumber = 0;
let score = 0;

function showQuestion() {
  const question = test[questionNumber];
  questionAsked.innerText = question.question;
}

function endGame() {
  const form = document.getElementById("playerAnswer");
  message.textContent = `Game Over!`;
  form.style.display = "none";
  question.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  showQuestion();

  const form = document.getElementById("playerAnswer");
  const message = document.getElementById("message");
  const playerInput = document.getElementById("answer");

  const playerName = localStorage.getItem("player");
  const scoreTracker = document.getElementById("score");
  scoreTracker.innerText = `Total score for Player, ${playerName}: ${score}`;

  form.addEventListener("submit", function (event) {
    let tempScore = 0;
    event.preventDefault();
    const checkAnswer = playerInput.value;
    tempScore += (50 - Math.abs(checkAnswer - test[questionNumber].answer)) * 2;
    if (tempScore <= 0) {
      tempScore = 0;
      message.textContent = `Your guess is off.....by a lot. Your Score is ${tempScore}`;
    } else {
      message.textContent = `Nice guess, your score is ${tempScore}`;
    }
    playerInput.value = "";
    score += tempScore;
    scoreTracker.innerText = `Total score for Player, ${playerName}: ${score}`;
    questionNumber++;
    if (questionNumber < test.length) {
      setTimeout(() => {
        showQuestion();
        message.textContent = "";
      }, 2000);
    } else {
      setTimeout(() => {
        endGame();
      }, 2500);
    }
  });
});
