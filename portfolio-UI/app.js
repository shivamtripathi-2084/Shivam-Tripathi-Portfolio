(function () {
  [...document.querySelectorAll(".control")].forEach((button) => {
    button.addEventListener("click", function () {
      document.querySelector(".active-btn").classList.remove("active-btn");
      this.classList.add("active-btn");
      document.querySelector(".active").classList.remove("active");
      document.getElementById(button.dataset.id).classList.add("active");
    });
  });
  document.querySelector(".theme-btn").addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
  });
})();

const contactForm = document.getElementById("contact-form");
const formStatus = document.getElementById("form-status");

contactForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = contactForm.querySelector('button[type="submit"]');
  const buttonText = submitButton.querySelector(".btn-text");
  const originalText = buttonText.textContent;

  submitButton.disabled = true;
  buttonText.textContent = "Sending...";
  formStatus.textContent = "Sending message...";

  const formData = new FormData(contactForm);

  const data = {
    name: (formData.get("name") || "").trim(),
    email: (formData.get("email") || "").trim(),
    subject: (formData.get("subject") || "").trim(),
    message: (formData.get("message") || "").trim(),
    website: (formData.get("website") || "").trim(),
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/api/contact", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "Unable to send your message.");
    }

    formStatus.textContent = result.message;
    contactForm.reset();
  } catch (error) {
    formStatus.textContent =
      error.message === "Failed to fetch"
        ? "Cannot connect to the server. Please try again."
        : error.message;
  } finally {
    submitButton.disabled = false;
    buttonText.textContent = originalText;
  }
});
