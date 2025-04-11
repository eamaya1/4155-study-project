/*const flashcards = [
    { question: "What is the capital of France?", answer: "Paris" },
    { question: "What is 2 + 2?", answer: "4" },
    { question: "What is the largest planet in our solar system?", answer: "Jupiter" }
];
*/
let currentCardIndex = 0;
let isFlipped = false;

function updateCard() {
    const front = document.getElementById("flashcard-front");
    const back = document.getElementById("flashcard-back");

    front.textContent = flashcards[currentCardIndex].question;
    back.textContent = flashcards[currentCardIndex].answer;

    // Reset flip state when updating the card
    isFlipped = false;
    document.querySelector(".flashcard-inner").classList.remove("flipped");
}

function flipCard() {
    isFlipped = !isFlipped;
    document.querySelector(".flashcard-inner").classList.toggle("flipped", isFlipped);
}

function nextCard() {
    if (currentCardIndex < flashcards.length - 1) {
        currentCardIndex++;
    } else {
        currentCardIndex = 0; // Loop back to first card
    }
    updateCard();
}

function prevCard() {
    if (currentCardIndex > 0) {
        currentCardIndex--;
    } else {
        currentCardIndex = flashcards.length - 1; // Loop to last card
    }
    updateCard();
}

// Initialize first card
updateCard();
