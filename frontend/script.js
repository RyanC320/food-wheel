let foods = []; // will be filled in by fetching from backend

async function loadFoods() {
  const response = await fetch("http://127.0.0.1:5000/foods");
  foods = await response.json();
}

loadFoods(); // run this immediately when the page loads

// Get references to the wheel, button, and result elements
const wheel = document.getElementById("wheel");
const spinBtn = document.getElementById("spin-btn");
const resultDiv = document.getElementById("result");

// Get references to the feedback buttons (thumbs up/down)
const feedbackButtons = document.getElementById("feedback-buttons");
const thumbsUpBtn = document.getElementById("thumbs-up");
const thumbsDownBtn = document.getElementById("thumbs-down");

// Get references for history feature
const showHistoryBtn = document.getElementById("show-history-btn");
const historyList = document.getElementById("history-list");

let currentRotation = 0; // tracks total rotation so it keeps spinning forward each time
let currentRestaurant = ""; // tracks what the wheel most recently landed on (for feedback)

// Code runs when spin button is clicked
spinBtn.addEventListener("click", () => {
  // 1. Pick a random food index (0 to foods.length - 1)
  const randomIndex = Math.floor(Math.random() * foods.length);

  // 2. Each slice size depends on how many foods we have
  const degreesPerSlice = 360 / foods.length;

  // 3. Calculate the angle needed to land on that slice
  //    We add extra full spins (like 5 full rotations) so it looks like it's really spinning
  const extraSpins = 5 * 360;
  const targetAngle = extraSpins + (randomIndex * degreesPerSlice);

  // 4. Update total rotation and apply it
  currentRotation += targetAngle;
  wheel.style.transform = `rotate(${currentRotation}deg)`;

  // 5. Clear old result and hide feedback buttons while spinning
  resultDiv.textContent = "";
  feedbackButtons.style.display = "none";

  // 6. After the animation finishes (4s, matching our CSS transition), show result
  setTimeout(() => {
  currentRestaurant = foods[randomIndex];
  resultDiv.textContent = `🍽️ You got: ${currentRestaurant}`;
  feedbackButtons.style.display = "block";

  // Log this spin to history
  fetch("http://127.0.0.1:5000/spin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ restaurant_name: currentRestaurant })
  });
}, 4000);
});

// Sends the user's feedback (like/dislike) to the backend
async function sendFeedback(liked) {
  await fetch("http://127.0.0.1:5000/feedback", {
    method: "POST", // POST because we're sending/saving data, not just requesting it
    headers: { "Content-Type": "application/json" }, // tells Flask we're sending JSON
    body: JSON.stringify({
      restaurant_name: currentRestaurant,
      liked: liked
    })
  });

  feedbackButtons.style.display = "none"; // hide buttons after voting
  resultDiv.textContent += " (Thanks for the feedback!)";
}

// When thumbs up is clicked, send feedback as "liked"
thumbsUpBtn.addEventListener("click", () => sendFeedback(true));

// When thumbs down is clicked, send feedback as "liked = false"
thumbsDownBtn.addEventListener("click", () => sendFeedback(false));

// Fetches and displays the last 10 spins
async function loadHistory() {
  const response = await fetch("http://127.0.0.1:5000/history");
  const history = await response.json();

  historyList.innerHTML = ""; // clear old list
  history.forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = `${entry.restaurant_name} - ${entry.spun_at}`;
    historyList.appendChild(li);
  });
}

showHistoryBtn.addEventListener("click", loadHistory);