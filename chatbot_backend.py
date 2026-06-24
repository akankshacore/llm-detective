from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

GAME_MASTER_PROMPT = """You are the game master AND all characters in a murder mystery game. 

At the very start of this conversation, you secretly generated a complete case. You must NEVER reveal the killer, weapon, or motive directly — only through the characters' answers.

=== YOUR SECRET CASE FILE (never reveal this directly) ===
{case_file}
=== END CASE FILE ===

## YOUR ROLES

**As NARRATOR**: When the player asks meta questions or needs scene-setting, respond as the narrator in italics using *asterisks*.

**As each SUSPECT**: When the player interrogates a suspect, YOU become that character completely. Speak in first person, in their voice and personality. Each suspect:
- Knows their own alibi (true or false)
- Knows surface-level facts about other suspects
- Has emotional reactions (nervous, defensive, sad, smug)
- May lie or deflect if they are the killer
- Will never directly admit to being the killer unless cornered with specific evidence

## STRICT RULES
1. NEVER contradict anything you've said before — the conversation history is your memory
2. The killer will give vague alibis, become defensive under pressure, and deflect suspicion
3. Innocent suspects may have minor secrets (embarrassing, not criminal) to hide
4. Give YES/NO for direct yes/no questions, but always add flavor
5. Drop subtle clues naturally — a nervous tic mention, a timeline inconsistency, a detail that doesn't quite fit
6. If asked something a character wouldn't know, they say so
7. Keep responses under 120 words — punchy, atmospheric, in-character

## RESPONSE FORMAT
Always start your response with the character name speaking:
[NARRATOR]: *...*
[SUSPECT NAME]: "..."

This is a game. Be dramatic, atmospheric, fun. Make the player feel like they're in a 1920s drawing room or a noir detective story.
"""

CASE_GENERATOR_PROMPT = """Generate a murder mystery case file for a text-based detective game. 

Return ONLY a structured case file in this exact format — no preamble, no extra text:

SETTING: [Evocative 1-sentence location + time period, e.g. "Ashworth Manor, English countryside, 1932"]

VICTIM: [Full name, age, occupation, 1-sentence personality]

KILLER: [Full name — must be one of the 4 suspects]

MURDER WEAPON: [Specific object]

MOTIVE: [2 sentences explaining why the killer did it]

HOW IT HAPPENED: [3 sentences describing exactly what happened — time, method, how they covered it up]

SUSPECTS:
1. [Full name] | [Age] | [Occupation] | [Personality in 10 words] | [Their alibi — true or false, note which] | [One secret they're hiding that's embarrassing but not the murder]
2. [Full name] | [Age] | [Occupation] | [Personality in 10 words] | [Their alibi — true or false, note which] | [One secret they're hiding]
3. [Full name] | [Age] | [Occupation] | [Personality in 10 words] | [Their alibi — true or false, note which] | [One secret they're hiding]
4. [Full name] | [Age] | [Occupation] | [Personality in 10 words] | [Their alibi — true or false, note which] | [One secret they're hiding]

KEY CLUES HIDDEN IN THE SCENE:
- [Clue 1 — physical object or observation]
- [Clue 2]
- [Clue 3]
- [Clue 4]

Make it atmospheric, intriguing, and solvable with careful interrogation. Make the killer non-obvious but fair."""


def get_llm():
    return ChatBedrockConverse(
        credentials_profile_name='default',
        region_name="us-east-1",
        model="us.amazon.nova-pro-v1:0",
        temperature=0.7,
        max_tokens=1000
    )


def generate_case_file():
    """Generate a fresh murder mystery case. Returns the raw case file string."""
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=CASE_GENERATOR_PROMPT)])
    return response.content


def parse_case_file(case_text):
    """Extract structured data from the raw case file for the UI."""
    data = {
        "setting": "",
        "victim": "",
        "suspects": [],
        "clues": [],
        "raw": case_text
    }

    lines = case_text.strip().split("\n")
    in_suspects = False
    in_clues = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("SETTING:"):
            data["setting"] = line.replace("SETTING:", "").strip()
        elif line.startswith("VICTIM:"):
            data["victim"] = line.replace("VICTIM:", "").strip()
        elif line.startswith("SUSPECTS:"):
            in_suspects = True
            in_clues = False
        elif line.startswith("KEY CLUES"):
            in_clues = True
            in_suspects = False
        elif in_suspects and line and line[0].isdigit() and "." in line[:3]:
            parts = line.split("|")
            name_part = parts[0].strip()
            # Remove leading "1. ", "2. " etc
            name = name_part.split(".", 1)[-1].strip() if "." in name_part else name_part
            data["suspects"].append(name)
        elif in_clues and line.startswith("-"):
            data["clues"].append(line[1:].strip())

    return data


def init_game_memory(case_file_text):
    """Create the system message + initial memory for a new game."""
    system = SystemMessage(content=GAME_MASTER_PROMPT.format(case_file=case_file_text))
    return [system]


def ask_suspect(question, suspect_name, memory):
    """Send a question directed at a specific suspect. Updates memory in place."""
    llm = get_llm()

    full_question = f"[Addressing {suspect_name}]: {question}"
    messages = memory + [HumanMessage(content=full_question)]

    response = llm.invoke(messages)

    memory.append(HumanMessage(content=full_question))
    memory.append(AIMessage(content=response.content))

    return response.content


def make_accusation(killer_name, weapon, motive, memory, case_file_text):
    """Player makes their final accusation. Returns the reveal."""
    llm = get_llm()

    accusation_prompt = f"""[PLAYER ACCUSATION]: I accuse {killer_name} of the murder, with {weapon}, motivated by {motive}.

As the NARRATOR, dramatically reveal whether they are correct. 
- If CORRECT: Describe the full reveal — what happened, how the killer did it, and which clues the player might have missed. Make it cinematic.
- If INCORRECT: Say they're wrong, give ONE small hint without revealing the killer, and tell them the game continues.

The actual case file is: {case_file_text}"""

    messages = memory + [HumanMessage(content=accusation_prompt)]
    response = llm.invoke(messages)

    memory.append(HumanMessage(content=accusation_prompt))
    memory.append(AIMessage(content=response.content))

    return response.content