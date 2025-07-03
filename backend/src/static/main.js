// Word rotation
const words = ["day", "week", "month"];
let wordIndex = 0;
setInterval(() => {
  wordIndex = (wordIndex + 1) % words.length;
  document.getElementById("rotate-word").textContent = words[wordIndex];
}, 2000);

// Scroll animation
const fadeEls = document.querySelectorAll(".fade-in");
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
});
fadeEls.forEach(el => observer.observe(el));

// Form handling
const form = document.getElementById("subscribe-form");
const emailInput = document.getElementById("email-input");
const responseMessage = document.getElementById("response-message");
const domain = "https://grub-poem-ai.onrender.com"

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  responseMessage.textContent = "";
  responseMessage.className = "mt-4 text-sm";

  if (!email) {
    responseMessage.textContent = "Please enter a valid email.";
    responseMessage.classList.add("text-red-500");
    return;
  }

  try {
    const res = await fetch(`${domain}/subscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    const data = await res.json();

    if (res.ok) {
      responseMessage.textContent = data.message || "Subscribed!";
      responseMessage.classList.add("text-green-600");
      form.reset();
    } else {
      responseMessage.textContent = data.detail || "Subscription failed.";
      responseMessage.classList.add("text-red-500");
    }
  } catch (err) {
    console.error(err);
    responseMessage.textContent = "Something went wrong. Try again.";
    responseMessage.classList.add("text-red-500");
  }
});
