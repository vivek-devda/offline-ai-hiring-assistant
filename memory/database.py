from collections import deque
import sqlite3

# short-term memory
memory = deque(maxlen=5)

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect(
    "memory.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    bot_response TEXT
)
""")

conn.commit()

# -------------------------------
# MEMORY FILTER
# -------------------------------
def is_valid_memory(text):

    # reject very short input
    if len(text.strip()) < 3:
        return False

    blocked = [
        ".venv",
        "scripts",
        "python.exe",
        "d:\\",
        "ps ",
        "traceback"
    ]

    for word in blocked:

        if word in text.lower():
            return False

    return True


# -------------------------------
# ADD MEMORY
# -------------------------------
def add_to_memory(user, bot):

    if is_valid_memory(user):

        # runtime memory
        memory.append((user, bot))

        # persistent database memory
        cursor.execute(
            "INSERT INTO interactions (user_input, bot_response) VALUES (?, ?)",
            (user, bot)
        )

        conn.commit()


# -------------------------------
# GET MEMORY
# -------------------------------
def get_memory():

    cursor.execute("""
        SELECT user_input, bot_response
        FROM interactions
        ORDER BY id DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    return rows