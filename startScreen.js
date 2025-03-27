function storeName(event) {
    event.preventDefault();
    const playerName = document.getElementById('player').value;
    localStorage.setItem('player', playerName);

    const playerForm = document.querySelector('#player-form');
    const startButton = document.createElement('button');
    startButton.innerText = "Guess Away"
    startButton.style.fontSize = '30px';
    startButton.style.backgroundColor = 'black';
    startButton.style.color = 'white';
    startButton.style.border = 'none';
    startButton.style.cursor = 'pointer';
    playerForm.innerHTML = ``;
    playerForm.appendChild(startButton);
    
    startButton.addEventListener('click', selectionPage);
}

function selectionPage() {
    window.location.href = "weatherGame.html"
}

document.getElementById('player-form').addEventListener('submit', storeName);