"""Live dashboard metrics updated when resumes are screened."""

total_resumes = 0
selected_candidates = 0
moderate_candidates = 0 
rejected_candidates = 0
all_scores: list[int] = []


def record_analysis(ats_score: int, status: str) -> None:
    global total_resumes, selected_candidates, moderate_candidates, rejected_candidates
    total_resumes += 1
    all_scores.append(ats_score)

    if status == "Rejected":
        rejected_candidates += 1
    elif status == "Moderate Match" or (40 <= ats_score < 60):
        moderate_candidates += 1  
    elif ats_score >= 60 or status in ("Highly Selected", "Selected"):
        selected_candidates += 1
    else:
        rejected_candidates += 1


def get_dashboard_data() -> dict:
    avg = int(sum(all_scores) / len(all_scores)) if all_scores else 0
    under_review = max(0, total_resumes - selected_candidates - moderate_candidates - rejected_candidates)
    return {
        "total_resumes": total_resumes,
        "selected_candidates": selected_candidates,
        "moderate_candidates": moderate_candidates,  
        "rejected_candidates": rejected_candidates,
        "under_review": under_review,
        "average_ats_score": avg,
    }