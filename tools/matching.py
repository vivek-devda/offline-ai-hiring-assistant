from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.skills import extract_skills
# -------------------------------
# JOB MATCHING TOOL (NEW)
# -------------------------------
def match_job(resume_text, job_text):

    # extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    if not resume_skills or not job_skills:
        return 0, []

    # convert skill lists into strings
    resume_data = " ".join(resume_skills)
    job_data = " ".join(job_skills)

    # TF-IDF
    documents = [resume_data, job_data]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # similarity score
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    tfidf_score = similarity[0][0] * 100

    # matched skills
    matched_skills = list(
        set(resume_skills) & set(job_skills)
    )

    # skill overlap score
    overlap_score = (
        len(matched_skills) / len(job_skills)
    ) * 100

    # final weighted score
    final_score = (
        0.7 * overlap_score
        +
        0.3 * tfidf_score
    )

    return round(final_score, 2), matched_skills