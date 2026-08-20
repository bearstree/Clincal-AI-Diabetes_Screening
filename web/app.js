const form = document.querySelector("#risk-form");
const status = document.querySelector("#form-status");
const result = document.querySelector("#result");
const submit = document.querySelector("#submit");
const apiBase = document.querySelector('meta[name="api-base-url"]').content.replace(/\/$/, "");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  status.textContent = "Estimating…";
  result.hidden = true;
  submit.disabled = true;
  const data = new FormData(form);
  const payload = {
    age_years: Number(data.get("age_years")), waist_cm: Number(data.get("waist_cm")),
    physically_active: data.get("physically_active") === "true", diastolic_bp: Number(data.get("diastolic_bp")),
  };
  try {
    const response = await fetch(`${apiBase}/v1/predict`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    if (!response.ok) throw new Error(response.status === 422 ? "Check the input ranges." : "The service is unavailable.");
    const prediction = await response.json();
    document.querySelector("#probability").textContent = `${(prediction.probability * 100).toFixed(1)}%`;
    document.querySelector("#interpretation").textContent = prediction.above_validation_threshold ? "Above the model’s validation threshold for this research outcome." : "Below the model’s validation threshold for this research outcome.";
    document.querySelector("#model-version").textContent = prediction.model_version;
    document.querySelector("#threshold").textContent = `${(prediction.threshold * 100).toFixed(1)}%`;
    result.hidden = false; status.textContent = "Estimate complete.";
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) { status.textContent = error instanceof Error ? error.message : "Unexpected error."; }
  finally { submit.disabled = false; }
});
