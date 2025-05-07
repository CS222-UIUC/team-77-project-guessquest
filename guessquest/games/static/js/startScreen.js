const text = "GuessQuest?";
const guessTextDiv = document.getElementById("startText");
let index = 0;

function revealNextLetter() {
  if (index < text.length) {
    guessTextDiv.textContent = text.substring(0, index + 1);
    index++;
    setTimeout(revealNextLetter, 200);
  } else {
    document.getElementById("player-form").style.display = "block";
  }
}

setTimeout(revealNextLetter, 600);
