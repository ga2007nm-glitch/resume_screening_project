import argparse
import sys
import json
from resume_analyzer import analyze_resume_text, extract_text

def main():
    parser = argparse.ArgumentParser(description="AI Resume Screening CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Path to resume file (PDF, TXT, DOCX)")
    group.add_argument("--text", "-t", help="Raw resume text")
    parser.add_argument("--json", "-j", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.file:
        try:
            resume_text = extract_text(args.file)
            if not resume_text.strip():
                print(json.dumps({"error": f"Could not read text from {args.file}"}) if args.json else f"Error: Could not read text from {args.file}", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": str(e)}) if args.json else f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        resume_text = args.text

    result = analyze_resume_text(resume_text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 50)
        print("AI Resume Screening System - Analysis Result")
        print("=" * 50)
        print(f"ATS Score:        {result['ats_score']}%")
        print(f"Status:           {result['status']}")
        print(f"Feedback:         {result['feedback']}")
        print("-" * 50)
        print(f"Matched Skills:   {', '.join(result['matched_skills']) if result['matched_skills'] else 'None'}")
        print(f"Missing Skills:   {', '.join(result['missing_skills']) if result['missing_skills'] else 'None'}")
        print(f"Recommended Co:   {', '.join(result['recommended_companies']) if result['recommended_companies'] else 'None'}")
        print(f"Suggested Roles:  {', '.join(result['recommended_roles']) if result['recommended_roles'] else 'None'}")
        print("=" * 50)

if __name__ == "__main__":
    main()
