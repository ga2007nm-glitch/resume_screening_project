let chartInstance = null;

function updateUI(data) {
    if (document.getElementById("totalResumes")) document.getElementById("totalResumes").innerText = data.total_resumes || 0;
    if (document.getElementById("selected")) document.getElementById("selected").innerText = data.selected_candidates || 0;
    if (document.getElementById("rejected")) document.getElementById("rejected").innerText = data.rejected_candidates || 0;
    if (document.getElementById("avgScore")) document.getElementById("avgScore").innerText = (data.average_ats_score || 0) + "%";
    if (document.getElementById("moderateCandidates")) document.getElementById("moderateCandidates").innerText = data.moderate_candidates || 0;

    const chartData = [
        data.total_resumes || 0,
        data.selected_candidates || 0,
        data.moderate_candidates || 0,
        data.rejected_candidates || 0,
        data.under_review || 0,
    ];

    const chartCanvas = document.getElementById("dashChart");
    if (!chartCanvas) return;

    if (chartInstance) {
        chartInstance.data.datasets[0].data = chartData;
        chartInstance.update();
    } else {
        chartInstance = new Chart(chartCanvas, {
            type: "bar",
            data: {
                labels: ["Total", "Selected", "Moderate Match", "Rejected", "Under Review"],
                datasets: [{
                    label: "Candidates",
                    data: chartData,
                    backgroundColor: ["#38bdf8", "#22c55e", "#f97316", "#ef4444", "#f59e0b"],
                    borderRadius: 8,
                }],
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });
    }
}

if (window.EventSource) {
    const es = new EventSource("/api/dashboard-stream");
    es.onmessage = (evt) => { try { updateUI(JSON.parse(evt.data)); } catch (e) {} };
    es.onerror = () => { es.close(); fetch("/api/dashboard").then(r => r.json()).then(updateUI); };
} else {
    fetch("/api/dashboard").then(r => r.json()).then(updateUI);
}