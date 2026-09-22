document.getElementById("screeningForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("resumeInput");
    const textInput = document.getElementById("resumeText");
    const resultSection = document.getElementById("resultSection");
    const loadingSection = document.getElementById("loadingSection");

    // Hide previous results and show loading spinner
    if (resultSection) resultSection.style.display = "none";
    if (loadingSection) loadingSection.style.display = "block";

    let response;
    
    try {
        // 1. Handle File Upload routing
        if (fileInput.files.length > 0) {
            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            response = await fetch("/api/analyze-resume", {
                method: "POST",
                body: formData
            });
        } 
        // 2. Handle Text Input routing
        else if (textInput.value.trim() !== "") {
            const formData = new FormData();
            formData.append("text", textInput.value);

            response = await fetch("/api/analyze-text", {
                method: "POST",
                body: formData
            });
        } 
        // 3. Neither option selected
        else {
            alert("Please upload a file or paste your resume text first.");
            if (loadingSection) loadingSection.style.display = "none";
            return;
        }

        if (!response.ok) {
            throw new Error(`Failed to process screening request. Status: ${response.status}`);
        }

        const data = await response.json();

        // Update ATS Score value
        const scoreVal = document.getElementById("atsScoreValue");
        if (scoreVal) scoreVal.innerText = (data.ats_score || 0) + "%";

        // Render Matched Skills (With custom pill styling padding to keep badges clean)
        const matchedBox = document.getElementById("matchedSkillsBox");
        if (matchedBox) {
            matchedBox.innerHTML = "";
            if (data.matched_skills && data.matched_skills.length > 0) {
                data.matched_skills.forEach(skill => {
                    matchedBox.innerHTML += `<span class="skill-pill" style="background: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: 500;">${skill}</span>`;
                });
            } else {
                matchedBox.innerHTML = `<span style="color: #64748b; font-style: italic;">No specific matches found.</span>`;
            }
        }

        // Render Missing Skills (With custom pill styling padding to keep badges clean)
        const missingBox = document.getElementById("missingSkillsBox");
        if (missingBox) {
            missingBox.innerHTML = "";
            if (data.missing_skills && data.missing_skills.length > 0) {
                data.missing_skills.forEach(skill => {
                    missingBox.innerHTML += `<span class="skill-pill" style="background: #fee2e2; color: #b91c1c; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: 500;">${skill}</span>`;
                });
            } else {
                missingBox.innerHTML = `<span style="color: #64748b; font-style: italic;">Perfect! No major skill gaps identified.</span>`;
            }
        }

        // FIXED: Extract and render Recommended Job Roles directly to the layout
        const rolesBox = document.getElementById("rolesPlacementBox");
        if (rolesBox) {
            rolesBox.innerHTML = "";
            // Maps to backend array value 'recommended_roles' or 'job_roles'
            const jobRoles = data.recommended_roles || data.job_roles;
            if (jobRoles && jobRoles.length > 0) {
                jobRoles.forEach(role => {
                    rolesBox.innerHTML += `<span class="role-pill" style="background: #f1f5f9; color: #334155; padding: 6px 14px; border-radius: 6px; font-size: 14px; border: 1px solid #e2e8f0; font-weight: 500;">${role}</span>`;
                });
            } else {
                rolesBox.innerHTML = `<span style="color: #64748b; font-style: italic;">No specific job roles matching this text.</span>`;
            }
        }

        // Render Recommended Companies
        const companiesBox = document.getElementById("companiesPlacementBox");
        if (companiesBox) {
            companiesBox.innerHTML = "";
            if (data.recommended_companies && data.recommended_companies.length > 0) {
                data.recommended_companies.forEach(company => {
                    companiesBox.innerHTML += `
                        <div class="company-card">
                            <i class="fa-solid fa-building"></i> ${company}
                        </div>`;
                });
            } else {
                companiesBox.innerHTML = `<div class="company-card"><i class="fa-solid fa-circle-exclamation"></i> Standard Roles Apply</div>`;
            }
        }

        // Reveal the result card panel
        if (resultSection) resultSection.style.display = "block";

    } catch (error) {
        console.error("Screening Error:", error);
        alert("An error occurred while analyzing the resume. Please check your backend server terminal.");
    } finally {
        // Always turn off the loading animation spinner
        if (loadingSection) loadingSection.style.display = "none";
    }
});