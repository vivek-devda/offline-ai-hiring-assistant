from tools.outreach import (
    generate_outreach,
    generate_summary
)
from memory.database import (
    add_to_memory,
    get_memory,
    is_valid_memory
)
import json
from tools.pdf_tools import extract_pdf_text
import re
from fuzzywuzzy import fuzz
from tools.matching import match_job



# -------------------------------
# LOAD RESPONSES
# -------------------------------
def load_responses(file="responses.json"):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: responses.json file not found.")
        return {}


# -------------------------------
# PREPROCESSING
# -------------------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


# -------------------------------
# INTENT DETECTION
# -------------------------------
def detect_intent(user_input, responses):
    best_match = None
    best_score = 0

    for key in responses:
        score = fuzz.ratio(user_input, key)

        if score > best_score:
            best_score = score
            best_match = key

    return {
        "intent": best_match,
        "confidence": best_score
    }

# -------------------------------
# DECISION ENGINE (ADD THIS HERE)
# -------------------------------
def decide(intent_data):
    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    if confidence < 75:
        return "clarify"

    if intent and ("document" in intent or "pdf" in intent):
        return "pdf_search"
    if intent and ("match" in intent or "job" in intent):
        return "job_match"

    return "respond"

# -------------------------------
# CHAT LOOP (FIXED)
# -------------------------------
def chatbot():
    responses = load_responses()

    print("Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").lower()
        if not user_input.strip():
            print("Bot: Please enter something.")
            continue
        if user_input == "exit":
            print("Bot: Goodbye!")
            break
        # preprocess
        user_input = preprocess(user_input)
        # ---------------- MEMORY RECALL ----------------
        if any(phrase in user_input for phrase in [
    "what did i ask",
    "what did i say",
    "what did i talk",
    "previous question",
    "earlier"
]):
            past = get_memory()
            if not past:
                print("Bot: I don't remember anything yet.")
            else:
                print("Bot: You asked:")
                for item in past:
                    print("-", item[0])

            continue
        # intent detection
        # -------- DECISION LOGIC --------
        if "job" in user_input and "match" in user_input:
            intent_data = {"intent": "job_match", "confidence": 100}
            action = "job_match"
        else:
            intent_data = detect_intent(user_input, responses)
            action = decide(intent_data)
        # ---------------- ACTION HANDLING ----------------

        # 🔹 1. CLARIFY
        if action == "clarify":

            response = "Can you clarify your question?"

            print("Bot:", response)

            add_to_memory(user_input, response)

        # 🔹 2. PDF SEARCH
        elif action == "pdf_search":

            text = extract_pdf_text("your_file.pdf")

            if any(word in text.lower() for word in user_input.split()):

                response = "I found something related in your document."

            else:

                response = "I searched the document but found nothing relevant."

            print("Bot:", response)

            add_to_memory(user_input, response)

        # 🔹 3. JOB MATCH
        elif action == "job_match":

            print("Bot: Enter resume text:")
            resume_text = input("Resume: ")
            if resume_text.lower() == "exit":
                print("Bot: Job matching cancelled.")
                continue

            print("Bot: Enter job description:")
            job_text = input("Job: ")
            if job_text.lower() == "exit":
                print("Bot: Job matching cancelled.")
                continue

            # validate inputs
            if not resume_text.strip() or not job_text.strip():

                response = "Resume or job description cannot be empty."

                print("Bot:", response)

                add_to_memory(user_input, response)

                continue

            # run matching
            score, keywords = match_job(resume_text, job_text)

            # generate outreach message
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
                
            # generate candidate summary
            summary = generate_summary(
                resume_text,
                job_text,
                keywords,
                score
            )    
            
            # create response
            response = (
                f"Match Score: {score}%\n"
                f"Matched Keywords: {', '.join(keywords)}\n\n"
                f"Candidate Summary:\n"
                f"{summary}\n\n"
                f"Generated Outreach Message:\n\n"
                f"{outreach}"
            )

            # print result
            print("Bot:", response)

            # store useful memory
            memory_input = (
                f"Resume: {resume_text} | Job: {job_text}"
            )

            add_to_memory(memory_input, response)

        # 🔹 4. NORMAL RESPONSE
        else:

            intent = intent_data["intent"]

            response = responses[intent]

            print("Bot:", response)

            add_to_memory(user_input, response)
# RUN
# -------------------------------
if __name__ == "__main__":
    chatbot()