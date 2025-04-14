let questionIdx = 0;
const questionList = [
	{
		question: "Like a Rolling Stone",
		choices: ["Bob Dylan", "Marvin Gaye", "Stevie Wonder", "Selena Gomez"],
		answer: "Bob Dylan"
	},
	{
		question: "Strawberry Fields Forever",
		choices: ["Fleetwood Mac", "The Beatles", "Aretha Franklin", "Ariana Grande"],
		answer: "The Beatles"
	},
	{
		question: "Bohemian Rapsody",
		choices: ["Billie Holiday", "John Lennon", "Queen", "Madonna"],
		answer: "Queen"
	}
];
let score = 0;

function newGame() {
  questionIdx = 0;
  score = 0;
  document.getElementById("score").textContent = `Score: ${score}`;
  game();
}

function game() {
  const question = questionList[questionIdx].question;
  const answer = questionList[questionIdx].answer;
  const options = questionList[questionIdx].choices;

  document.getElementById("question").textContent = question;
  document.getElementById("options").innerHTML = "";
  options.forEach((option) => {
    const button = document.createElement("button");
    button.textContent = option;
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
  if (questionIdx < 3) {
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
  newGame();
}

newGame();