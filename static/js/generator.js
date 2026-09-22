const genForm = document.getElementById("generatorForm");
const output = document.getElementById("generatedResume");

genForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    output.innerHTML = '<div class="loading"><i class="fa-solid fa-spinner fa-spin"></i> Generating...</div>';

    try {
        const res = await fetch("/api/generate-resume", { method: "POST", body: new FormData(genForm) });
        const data = await res.json();
        output.innerHTML = `
            <div class="alert alert-success">${data.message}</div>
            <pre id="resumeText">${data.resume_text}</pre>
            <div class="btn-row">
                <button type="button" onclick="copyResume()"><i class="fa-solid fa-copy"></i> Copy</button>
                <button type="button" onclick="downloadResume()"><i class="fa-solid fa-download"></i> Download TXT</button>
            </div>`;
        updateNotificationBadge();
    } catch (_) {
        output.innerHTML = '<div class="alert alert-error">Failed to generate resume.</div>';
    }
});

function copyResume() {
    navigator.clipboard.writeText(document.getElementById("resumeText").textContent)
        .then(() => alert("Resume copied!"));
}

function downloadResume() {
    const blob = new Blob([document.getElementById("resumeText").textContent], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "resume.txt";
    a.click();
}
