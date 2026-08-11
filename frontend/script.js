// 8 foods matching the 8 slices in the wheel (order matters!)
// Array of food names
const foods = [
  "Pizza",
  "Sushi",
  "Burger",
  "Tacos",
  "Ramen",
  "Salad",
  "Pasta",
  "Fried Chicken"
];
// Get references to the wheel and spin button elements
const wheel = document.getElementById("wheel");
const spinBtn = document.getElementById("spin-btn");
const resultDiv = document.getElementById("result");

let currentRotation = 0; // tracks total rotation so it keeps spinning forward each time

// Code runs when button is clicked
spinBtn.addEventListener("click", () => {
  // 1. Pick a random food index (0 to 7)
  const randomIndex = Math.floor(Math.random() * foods.length);

  // 2. Each slice is 360/8 = 45 degrees
  const degreesPerSlice = 360 / foods.length;

  // 3. Calculate the angle needed to land on that slice
  //    We add extra full spins (like 5 full rotations) so it looks like it's really spinning
  const extraSpins = 5 * 360;
  const targetAngle = extraSpins + (randomIndex * degreesPerSlice);

  // 4. Update total rotation and apply it
  currentRotation += targetAngle;
  wheel.style.transform = `rotate(${currentRotation}deg)`;

  // 5. After the animation finishes (4s, matching our CSS transition), show result

resultDiv.textContent = ""; // clear old result while spinning

setTimeout(() => {
  resultDiv.textContent = `🍽️ You got: ${foods[randomIndex]}`;
}, 4000);
});