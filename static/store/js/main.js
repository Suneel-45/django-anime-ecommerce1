document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".message-close").forEach((button) => {
    button.addEventListener("click", () => button.closest(".message")?.remove());
  });

  // Avoid accidental duplicate checkout submissions.
  document.querySelectorAll('form[action*="checkout"], .form-card form').forEach((form) => {
    form.addEventListener("submit", () => {
      const submit = form.querySelector('button[type="submit"]');
      if (submit && form.checkValidity()) {
        submit.disabled = true;
        submit.dataset.originalText = submit.textContent;
        submit.textContent = "Please wait…";
      }
    });
  });

  // Client-side convenience only; Django validates all values server-side too.
  document.querySelectorAll('input[type="number"][name="quantity"]').forEach((input) => {
    input.addEventListener("change", () => {
      const min = Number(input.min || 0);
      const max = Number(input.max || 999);
      let value = Number(input.value);
      if (!Number.isFinite(value)) value = min;
      input.value = Math.max(min, Math.min(max, value));
    });
  });
});
