from flask import Flask, render_template, request
from tools.matching import match_job

from tools.outreach import (
    generate_outreach,
    generate_summary
)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        resume_text = request.form["resume"]
        job_text = request.form["job"]

        score, keywords = match_job(
            resume_text,
            job_text
        )

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

    return render_template(
        "index.html",
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)