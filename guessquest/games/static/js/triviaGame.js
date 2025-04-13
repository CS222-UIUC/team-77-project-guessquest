let questionIdx = 0;
let questionList = [];
let score = 0;

async function getQuestions() {
  try {
    const response = await fetch(
      "https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple"
    );
    const data = await response.json();
    questionList = data.results;
    newGame();
  } catch (error) {
    console.error("Error fetching data");
  }
}

function decodeHTML(text) {
  const doc = new DOMParser().parseFromString(text, "text/html");
  return doc.documentElement.textContent || doc.documentElement.innerText;
}

function newGame() {
  questionIdx = 0;
  questionList.clear;
  score = 0;
  document.getElementById("score").textContent = `Score: ${score}`;
  game();
}

function game() {
  const displayQuestion = questionList[questionIdx];
  const question = decodeHTML(displayQuestion.question);
  const answer = displayQuestion.correct_answer;
  const incorrect_answer = displayQuestion.incorrect_answers;
  const options = [
    answer,
    incorrect_answer[0],
    incorrect_answer[1],
    incorrect_answer[2],
  ];
  for (let i = options.length - 1; i > 0; i--) {
    const num = Math.floor(Math.random() * (i + 1));
    [options[i], options[num]] = [options[num], options[i]];
  }

  document.getElementById("question").textContent = question;
  document.getElementById("options").innerHTML = "";
  options.forEach((option) => {
    const button = document.createElement("button");
    button.textContent = decodeHTML(option);
    button.onclick = () => checkAnswer(option, answer);
    document.getElementById("options").appendChild(button);
  });
}

function checkAnswer(choice, answer) {
  if (choice == answer) {
    score += 10;
    document.getElementById("score").textContent = `Score: ${score}`;
  }
  questionIdx++;
  if (questionIdx < questionList.length) {
    game();
  } else {
    endGame();
  }
}

function endGame() {
  document.querySelector(".question-body").classList.add("hidden");
  document.querySelector(".restart").classList.remove("hidden");
  document.getElementById("question").textContent = "";
  document.getElementById("options").innerHTML = "";
  document.getElementById("score").textContent = `Final Score: ${score}`;
}

function restartGame() {
  document.querySelector(".question-body").classList.remove("hidden");
  document.querySelector(".restart").classList.add("hidden");
  document.getElementById("score").textContent = "";
  getQuestions();
}

window.onload = getQuestions();
