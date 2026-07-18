// Game Configuration
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 400;

// Game State
let gameState = 'start'; // start, playing, paused, gameover
let score = 0;
let gameSpeed = 5;
let animationId;
let mapGenerationCount = 0;

// Dinosaur
const dino = {
    x: 50,
    y: 300,
    width: 50,
    height: 60,
    velocityY: 0,
    jumping: false,
    gravity: 0.8,
    jumpForce: -15,
    groundY: 300
};

// Obstacles
let obstacles = [];
let obstacleTimer = 0;
let obstacleInterval = 100;

// Ground
const ground = {
    x: 0,
    y: 360,
    width: canvas.width,
    height: 40
};

// DOM Elements
const startScreen = document.getElementById('start-screen');
const pauseScreen = document.getElementById('pause-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resumeBtn = document.getElementById('resume-btn');
const replayBtn = document.getElementById('replay-btn');
const saveScoreBtn = document.getElementById('save-score-btn');
const currentScoreEl = document.getElementById('current-score');
const finalScoreEl = document.getElementById('final-score');
const playerNameInput = document.getElementById('player-name');
const scoreList = document.getElementById('score-list');

// Event Listeners
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', togglePause);
resumeBtn.addEventListener('click', togglePause);
replayBtn.addEventListener('click', restartGame);
saveScoreBtn.addEventListener('click', saveScore);

document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'ArrowUp') {
        e.preventDefault();
        if (gameState === 'playing') {
            jump();
        } else if (gameState === 'start') {
            startGame();
        } else if (gameState === 'gameover') {
            restartGame();
        }
    }
    if (e.code === 'KeyP' || e.code === 'Escape') {
        if (gameState === 'playing') {
            togglePause();
        }
    }
});

canvas.addEventListener('click', () => {
    if (gameState === 'playing') {
        jump();
    }
});

// Game Functions
function startGame() {
    gameState = 'playing';
    score = 0;
    gameSpeed = 5;
    obstacles = [];
    obstacleTimer = 0;
    dino.y = dino.groundY;
    dino.velocityY = 0;
    dino.jumping = false;
    
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    pauseScreen.classList.add('hidden');
    
    gameLoop();
}

function togglePause() {
    if (gameState === 'playing') {
        gameState = 'paused';
        pauseScreen.classList.remove('hidden');
        cancelAnimationFrame(animationId);
    } else if (gameState === 'paused') {
        gameState = 'playing';
        pauseScreen.classList.add('hidden');
        gameLoop();
    }
}

function restartGame() {
    startGame();
}

function jump() {
    if (!dino.jumping) {
        dino.velocityY = dino.jumpForce;
        dino.jumping = true;
    }
}

function updateDino() {
    dino.velocityY += dino.gravity;
    dino.y += dino.velocityY;
    
    if (dino.y >= dino.groundY) {
        dino.y = dino.groundY;
        dino.velocityY = 0;
        dino.jumping = false;
    }
}

function generateObstacle() {
    // Randomize obstacle types based on map generation
    let types;
    if (mapGenerationCount === 0) {
        types = ['cactus', 'cactus', 'cactus', 'bird'];
    } else {
        // More variety as map generates
        types = ['cactus', 'cactus', 'bird', 'bird', 'rock'];
    }
    
    const type = types[Math.floor(Math.random() * types.length)];
    
    let obstacle = {
        x: canvas.width,
        y: type === 'bird' ? 250 : (type === 'rock' ? 320 : 310),
        width: type === 'bird' ? 40 : (type === 'rock' ? 35 : 30),
        height: type === 'bird' ? 30 : (type === 'rock' ? 40 : 50),
        type: type
    };
    
    obstacles.push(obstacle);
}

function updateObstacles() {
    obstacleTimer++;
    
    if (obstacleTimer >= obstacleInterval) {
        generateObstacle();
        obstacleTimer = 0;
        obstacleInterval = Math.random() * 50 + 70; // Random interval between 70-120
    }
    
    obstacles.forEach((obstacle, index) => {
        obstacle.x -= gameSpeed;
        
        if (obstacle.x + obstacle.width < 0) {
            obstacles.splice(index, 1);
            score += 10;
        }
    });
}

function checkCollision() {
    for (let obstacle of obstacles) {
        if (
            dino.x < obstacle.x + obstacle.width &&
            dino.x + dino.width > obstacle.x &&
            dino.y < obstacle.y + obstacle.height &&
            dino.y + dino.height > obstacle.y
        ) {
            return true;
        }
    }
    return false;
}

function gameOver() {
    gameState = 'gameover';
    cancelAnimationFrame(animationId);
    
    finalScoreEl.textContent = score;
    gameOverScreen.classList.remove('hidden');
}

function updateScore() {
    currentScoreEl.textContent = score;
    
    // Random map generation every 100 points
    if (score > 0 && score % 100 === 0 && score !== mapGenerationCount * 100) {
        mapGenerationCount++;
        console.log(`Map generated! Generation: ${mapGenerationCount}`);
        // Clear existing obstacles for new map feel
        obstacles = [];
    }
    
    // Increase game speed by 1% every 150 points
    if (score > 0 && score % 150 === 0) {
        gameSpeed = gameSpeed * 1.01; // 1% increase
        console.log(`Speed increased! New speed: ${gameSpeed.toFixed(2)}`);
    }
}

function drawDino() {
    ctx.fillStyle = '#333';
    
    // Body
    ctx.fillRect(dino.x, dino.y, dino.width, dino.height);
    
    // Eye
    ctx.fillStyle = 'white';
    ctx.fillRect(dino.x + 35, dino.y + 10, 8, 8);
    ctx.fillStyle = 'black';
    ctx.fillRect(dino.x + 38, dino.y + 12, 4, 4);
    
    // Legs
    ctx.fillStyle = '#333';
    if (dino.jumping) {
        ctx.fillRect(dino.x + 10, dino.y + dino.height, 10, 15);
        ctx.fillRect(dino.x + 30, dino.y + dino.height, 10, 15);
    } else {
        ctx.fillRect(dino.x + 10, dino.y + dino.height, 10, 10);
        ctx.fillRect(dino.x + 30, dino.y + dino.height, 10, 10);
    }
}

function drawObstacles() {
    obstacles.forEach(obstacle => {
        if (obstacle.type === 'cactus') {
            ctx.fillStyle = '#2E7D32';
            ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            
            // Cactus arms
            ctx.fillRect(obstacle.x - 10, obstacle.y + 10, 10, 20);
            ctx.fillRect(obstacle.x + obstacle.width, obstacle.y + 5, 10, 15);
        } else if (obstacle.type === 'bird') {
            ctx.fillStyle = '#E65100';
            ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            
            // Wings
            ctx.fillRect(obstacle.x + 5, obstacle.y - 10, 20, 10);
            ctx.fillRect(obstacle.x + 5, obstacle.y + obstacle.height, 20, 10);
        } else if (obstacle.type === 'rock') {
            ctx.fillStyle = '#696969';
            ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            
            // Rock details
            ctx.fillStyle = '#808080';
            ctx.fillRect(obstacle.x + 5, obstacle.y + 5, 10, 10);
            ctx.fillRect(obstacle.x + 20, obstacle.y + 15, 8, 8);
        }
    });
}

function drawGround() {
    ctx.fillStyle = '#8B4513';
    ctx.fillRect(ground.x, ground.y, ground.width, ground.height);
    
    // Ground details
    ctx.fillStyle = '#654321';
    for (let i = 0; i < canvas.width; i += 50) {
        ctx.fillRect(i, ground.y, 30, 5);
    }
}

function drawBackground() {
    // Sky gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#87CEEB');
    gradient.addColorStop(1, '#E0F6FF');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Clouds
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.beginPath();
    ctx.arc(100, 80, 30, 0, Math.PI * 2);
    ctx.arc(140, 80, 40, 0, Math.PI * 2);
    ctx.arc(180, 80, 30, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(400, 120, 25, 0, Math.PI * 2);
    ctx.arc(435, 120, 35, 0, Math.PI * 2);
    ctx.arc(470, 120, 25, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(650, 60, 20, 0, Math.PI * 2);
    ctx.arc(680, 60, 30, 0, Math.PI * 2);
    ctx.arc(710, 60, 20, 0, Math.PI * 2);
    ctx.fill();
}

function gameLoop() {
    if (gameState !== 'playing') return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBackground();
    drawGround();
    
    updateDino();
    updateObstacles();
    
    if (checkCollision()) {
        gameOver();
        return;
    }
    
    drawDino();
    drawObstacles();
    
    updateScore();
    
    animationId = requestAnimationFrame(gameLoop);
}

// Scoreboard Functions (using API with localStorage fallback)
function loadScores() {
    fetch('/api/scores')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayScores(data.scores);
            } else {
                console.error('Error loading scores:', data.message);
                fallbackToLocalStorage();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            fallbackToLocalStorage();
        });
}

function fallbackToLocalStorage() {
    const scores = JSON.parse(localStorage.getItem('dinoScores')) || [];
    displayScores(scores);
}

function displayScores(scores) {
    scoreList.innerHTML = '';
    
    if (scores.length === 0) {
        scoreList.innerHTML = '<li>No scores yet</li>';
        return;
    }
    
    scores.forEach((scoreData, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${index + 1}. ${scoreData.player_name}</span>
            <span>${scoreData.score}</span>
        `;
        scoreList.appendChild(li);
    });
}

function saveScore() {
    const playerName = playerNameInput.value.trim() || 'Anonymous';
    
    fetch('/api/scores', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player_name: playerName,
            score: score
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Score saved successfully!');
            playerNameInput.value = '';
            loadScores();
        } else {
            alert('Error saving score: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving score');
    });
}

// Initialize
loadScores();

// Draw initial state
drawBackground();
drawGround();
drawDino();
