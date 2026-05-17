import re
from fuzzywuzzy import fuzz
# -------------------------------
# KNOWN SKILLS DATABASE
# -------------------------------
SKILL_ALIASES = {
    "python": ["python", "py"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "sql": ["sql"],
    "flask": ["flask"],
    "django": ["django"],
    "data analysis": ["data analysis"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "java": ["java"],
    "c++": ["c++"],
    "javascript": ["javascript", "js"],
    "react": ["react"],
    "nodejs": ["nodejs", "node"],
    "ai": ["ai", "artificial intelligence"]
}

# -------------------------------
# SKILL EXTRACTION
# -------------------------------
def extract_skills(text):

    text = text.lower()

    words = text.split()

    found_skills = []

    for main_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            # exact whole-word match first
            pattern = r'\b' + re.escape(alias) + r'\b'

            if re.search(pattern, text):

                found_skills.append(main_skill)

                break

            # fuzzy matching for typos
            for word in words:

                similarity = fuzz.ratio(
                    word,
                    alias
                )

                # threshold
                if similarity >= 80:

                    found_skills.append(main_skill)

                    break

    return list(set(found_skills))