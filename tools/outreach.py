from nlp.skills import extract_skills

# -------------------------------
# OUTREACH MESSAGE GENERATOR
# -------------------------------
def generate_outreach(
    resume_text,
    job_text,
    matched_skills,
    score
):

    if score >= 70:
        level = "strong"
        fit_line = (
            "I believe your profile aligns very well with this role."
        )
        
    elif score >= 40:
        level = "moderate"
        fit_line = (
            "Your profile shows several relevant technical strengths for this role."
        )
        
    else:
        level = "limited"
        fit_line = (
            "There are currently only a few matching technical areas for this role."
        )

    skills_text = ", ".join(matched_skills)

    message = (
        f"Hi Candidate,\n\n"
        f"Your background in {skills_text} shows a {level} alignment "
        f"with this opportunity.\n\n"
        f"{fit_line}\n\n"
        f"Would you be interested in discussing this opportunity further?"
    )

    return message


# -------------------------------
# CANDIDATE SUMMARY GENERATOR
# -------------------------------
def generate_summary(
    resume_text,
    job_text,
    matched_skills,
    score
):

    summary_points = []

    # strength level
    if score >= 70:

        summary_points.append(
            "Strong overall alignment with the role."
        )

    elif score >= 40:

        summary_points.append(
            "Moderate alignment with the role."
        )

    else:

        summary_points.append(
            "Limited alignment with the role."
        )

    # matched skills
    if matched_skills:

        summary_points.append(
            "Matched technical skills: "
            + ", ".join(matched_skills)
        )

    # missing skills
    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_text)

    missing_skills = list(
        set(job_skills) - set(resume_skills)
    )

    if missing_skills:

        summary_points.append(
            "Missing Skills:\n• "
            + "\n• ".join(missing_skills)
        )

    # capability inference
    total_resume_skills = len(resume_skills)

    advanced_skills = [
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "ai"
    ]

    advanced_count = len(
        set(resume_skills) & set(advanced_skills)
    )

    # interpretation layer
    if score >= 70:

        summary_points.append(
            "Candidate appears strongly suited for this role."
        )

    elif score >= 40:

        summary_points.append(
            "Candidate has partial alignment but may need additional supporting skills."
        )

    else:

        summary_points.append(
            "Candidate currently lacks several core requirements for this role."
        )

    # capability reasoning
    if total_resume_skills >= 8:

        summary_points.append(
            "Candidate demonstrates broad technical exposure across multiple domains."
        )

    if advanced_count >= 3:

        summary_points.append(
            "Candidate shows strong exposure to advanced AI/ML technologies."
        )

    # overqualification reasoning
    if (
        total_resume_skills > len(job_skills) + 5
        and score >= 60
    ):

        summary_points.append(
            "Candidate may be overqualified relative to the current job requirements."
        )
        
    # final summary
    return "\n- " + "\n- ".join(summary_points)