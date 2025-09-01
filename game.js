// --- Game State ---
let skoins = 0;
let level = 1;
let character = "Adventurer";
let inventory = [];

const cases = [
  { tier: 1, price: 500, rewards: ["Ultra Rare Sword", "Legendary Character", "100 skoins", "Epic Armor", "Rare Gem"] },
  { tier: 2, price: 300, rewards: ["Rare Sword", "Rare Character", "60 skoins", "Rare Armor", "Gem"] },
  { tier: 3, price: 200, rewards: ["Uncommon Sword", "Uncommon Character", "40 skoins", "Uncommon Armor", "Crystal"] },
  { tier: 4, price: 120, rewards: ["Common Sword", "30 skoins", "Common Armor", "Stone"] },
  { tier: 5, price: 100, rewards: ["Basic Sword", "20 skoins", "Basic Armor", "Pebble"] }
];

function updateUI() {
  document.getElementById('skoins-count').textContent = skoins;
  document.getElementById('player-level').textContent = level;
  document.getElementById('character-name').textContent = character;
  document.getElementById('inventory-list').innerHTML = inventory.map(item => `<li>${item}</li>`).join('');
}

function generateArithmeticQuestion() {
  const types = [
    () => {
      let a = Math.floor(Math.random() * 200 + 10);
      let b = Math.floor(Math.random() * 10 + 2);
      return { q: `${a} / ${b}`, a: +(a / b).toPrecision(3) };
    },
    () => {
      let a = Math.floor(Math.random() * 50 + 10);
      let b = Math.floor(Math.random() * 200 + 10);
      return { q: `${a}% of ${b}`, a: +(b * a / 100).toPrecision(3) };
    },
    () => {
      let a = Math.floor(Math.random() * 100 + 1);
      let b = Math.floor(Math.random() * 100 + 1);
      return { q: `${a} + ${b}`, a: a + b };
    },
    () => {
      let a = Math.floor(Math.random() * 100 + 1);
      let b = Math.floor(Math.random() * 100 + 1);
      return { q: `${a} - ${b}`, a: a - b };
    },
    () => {
      let a = Math.floor(Math.random() * 30 + 2);
      let b = Math.floor(Math.random() * 10 + 2);
      return { q: `${a} x ${b}`, a: a * b };
    }
  ];
  const t = types[Math.floor(Math.random() * types.length)];
  return t();
}

let currentQuestion = null;

document.getElementById('new-question').onclick = () => {
  currentQuestion = generateArithmeticQuestion();
  document.getElementById('question-text').textContent = currentQuestion.q;
  document.getElementById('result-message').textContent = '';
  document.getElementById('answer-input').value = '';
};

document.getElementById('submit-answer').onclick = () => {
  if (!currentQuestion) return;
  let userAnswer = document.getElementById('answer-input').value.trim();
  let correct = Math.abs(Number(userAnswer) - Number(currentQuestion.a)) < 0.01;
  if (correct) {
    let reward = 10 + level * 2;
    skoins += reward;
    document.getElementById('result-message').textContent = `Correct! +${reward} skoins!`;
    currentQuestion = null;
  } else {
    document.getElementById('result-message').textContent = `Wrong! Correct answer: ${currentQuestion.a}`;
    currentQuestion = null;
  }
  updateUI();
};

document.getElementById('upgrade-level').onclick = () => {
  if (skoins >= 50) {
    level++;
    skoins -= 50;
    document.getElementById('action-message').textContent = "Level up! You are now level " + level;
  } else {
    document.getElementById('action-message').textContent = "Not enough skoins!";
  }
  updateUI();
};

document.getElementById('open-case').onclick = () => {
  let caseTier = 5; // default is cheapest
  for (let i = 0; i < cases.length; i++) {
    if (skoins >= cases[i].price) {
      caseTier = i + 1;
      break;
    }
  }
  const selectedCase = cases.find(c => c.tier === caseTier);
  if (!selectedCase || skoins < selectedCase.price) {
    document.getElementById('action-message').textContent = "Not enough skoins for any case!";
    return;
  }
  skoins -= selectedCase.price;
  // Random reward
  let rewardIndex = Math.floor(Math.random() * selectedCase.rewards.length);
  let reward = selectedCase.rewards[rewardIndex];
  inventory.push(reward);
  document.getElementById('action-message').textContent = `You opened a Tier ${caseTier} case and won: ${reward}!`;
  updateUI();
};

document.getElementById('battle').onclick = () => {
  if (skoins < 30) {
    document.getElementById('action-message').textContent = "Not enough skoins to battle!";
    return;
  }
  skoins -= 30;
  // Simple battle simulation
  let win = Math.random() < (0.5 + level * 0.01);
  if (win) {
    let prize = 50 + level * 5;
    skoins += prize;
    document.getElementById('action-message').textContent = `You won the battle! +${prize} skoins!`;
  } else {
    document.getElementById('action-message').textContent = `You lost the battle! Try again.`;
  }
  updateUI();
};

updateUI();
