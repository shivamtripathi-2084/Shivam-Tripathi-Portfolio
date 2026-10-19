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

// Local development URL.
// Before deployment, replace this with your Render API URL.
// const API_URL = "http://127.0.0.1:8000/api/contact";
const API_URL = "https://shivam-tripathi-portfolio.onrender.com/api/contact";

if (contactForm && formStatus) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitButton = contactForm.querySelector(
      'button[type="submit"]'
    );
    const buttonText = submitButton?.querySelector(".btn-text");
    const originalText = buttonText?.textContent || "Send Message";

    if (submitButton) submitButton.disabled = true;
    if (buttonText) buttonText.textContent = "Sending...";

    formStatus.textContent = "Sending message...";

    const formData = new FormData(contactForm);

    const data = {
      name: (formData.get("name") || "").toString().trim(),
      email: (formData.get("email") || "").toString().trim(),
      subject: (formData.get("subject") || "").toString().trim(),
      message: (formData.get("message") || "").toString().trim(),
      website: (formData.get("website") || "").toString().trim(),
    };

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail || "Unable to send your message."
        );
      }

      formStatus.textContent =
        result.message || "Your message has been sent successfully!";

      contactForm.reset();
    } catch (error) {
      console.error("Contact form error:", error);

      if (error instanceof TypeError) {
        formStatus.textContent =
          "Cannot connect to the server. Please try again.";
      } else {
        formStatus.textContent =
          error.message || "Something went wrong. Please try again.";
      }
    } finally {
      if (submitButton) submitButton.disabled = false;
      if (buttonText) buttonText.textContent = originalText;
    }
  });
}
