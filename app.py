from flask import Flask, render_template, request, send_from_directory
from tools.matching import match_job
from tools.pdf_tools import extract_pdf_text

from tools.outreach import (
    generate_outreach,
    generate_summary
)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def home():

    result = None
    selected_candidate = 0
    results = []

    if request.method == "POST":

        print(request.files)
        pdf_files = request.files.getlist("resume_pdfs")
        print("Number of resumes:", len(pdf_files))

        job_text = request.form["job"]
        selected_candidate = request.args.get(
            "candidate",
            default=0,
            type=int
        )
        
        for file in pdf_files:
            print(file.filename)
        for pdf_file in pdf_files:
            print("Processing:", pdf_file.filename)
            pdf_path = f"uploads/{pdf_file.filename}"
            pdf_file.save(pdf_path)
            resume_text = extract_pdf_text(pdf_path)
            print("Characters extracted:", len(resume_text))


            score, keywords = match_job(
            resume_text,
            job_text
        )
            print("Score:", score)
            print("Keywords:", keywords)
            
            # outreach logic
            if not keywords:

                outreach = (
                    "No strong technical alignment was detected "
                    "between the resume and job description."
                )

            else:

                outreach = generate_outreach(
                    resume_text,
                    job_text,
                    keywords,
                    score
                )

            # summary
            summary = generate_summary(
                resume_text,
                job_text,
                keywords,
                score
            )

            result = {
                "score": round(score, 2),
                "keywords": ", ".join(keywords),
                "summary": summary,
                "outreach": outreach
            }
            results.append({
                "score": round(score, 2),
                "keywords": ", ".join(keywords),
                "summary": summary,
                "outreach": outreach,
                "filename": pdf_file.filename,
                "filepath": pdf_path
            })
            
                
            
            

        
    if results:
        result = results[selected_candidate]

    return render_template(
        "index.html",
        result=result,
        results=results
    )
    
@app.route("/resume/<filename>")
def view_resume(filename):
    return send_from_directory(
        "uploads",
        filename
    )

if __name__ == "__main__":
    app.run(debug=True)