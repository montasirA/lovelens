(() => {
  const textarea = document.querySelector("[data-counter='analysis-counter']");
  const counter = document.getElementById("analysis-counter");
  if (!textarea || !counter) return;
  const update = () => {
    counter.textContent = textarea.value.length.toString();
  };
  textarea.addEventListener("input", update);
  update();
})();
