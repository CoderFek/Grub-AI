document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");
  const emailInput = document.getElementById("email");
  const responseText = document.getElementById("form-response");
  const domain = "https://grub-poem-ai.onrender.com";

  if (!token) {
    responseText.textContent = "Missing token.";
    responseText.classList.add("text-red-500");
    return;
  }

  try {
    const res = await fetch(`${domain}/api/verify-email?token=${token}`);
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Verification failed.");
    }

    emailInput.value = data.email;
  } catch (err) {
    responseText.textContent = err.message;
    responseText.classList.add("text-red-500");
  }

  const form = document.getElementById("frequency-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    responseText.textContent = "";

    try {
      const formData = new FormData(form);
      const body = new URLSearchParams(formData);

      const res = await fetch(`${domain}/set-frequency`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body
      });

      if (res.ok) {
        window.location.href = "/";
      } else {
        const data = await res.json();
        throw new Error(data.detail || "Failed to save frequency.");
      }
    } catch (err) {
      responseText.textContent = err.message;
      responseText.classList.add("text-red-500");
    }
  });
});
