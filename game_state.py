def new_game_state():
    return {
        "phase": "loading",        # loading | playing | accused | solved
        "case_file_text": "",      # raw AI-generated case text
        "case_data": {},           # parsed structured data
        "memory": [],              # LangChain message history
        "current_suspect": None,   # which suspect is selected
        "questions_asked": 0,      # total questions asked
        "clues_collected": [],     # player-saved clues (strings)
        "chat_log": [],            # list of {suspect, question, answer}
        "accusation_result": "",   # the reveal text
        "accused_correctly": None, # True/False/None
    }


def add_clue(state, clue_text):
    if clue_text and clue_text not in state["clues_collected"]:
        state["clues_collected"].append(clue_text)


def remove_clue(state, index):
    if 0 <= index < len(state["clues_collected"]):
        state["clues_collected"].pop(index)


def log_exchange(state, suspect, question, answer):
    state["chat_log"].append({
        "suspect": suspect,
        "question": question,
        "answer": answer,
    })
    state["questions_asked"] += 1