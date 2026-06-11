<div align="center">

```
██╗     ██╗     ███╗   ███╗    ██████╗ ███████╗████████╗███████╗ ██████╗████████╗██╗██╗   ██╗███████╗
██║     ██║     ████╗ ████║    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║██║   ██║██╔════╝
██║     ██║     ██╔████╔██║    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║██║   ██║█████╗  
██║     ██║     ██║╚██╔╝██║    ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║╚██╗ ██╔╝██╔══╝  
███████╗███████╗██║ ╚═╝ ██║    ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ██║ ╚████╔╝ ███████╗
╚══════╝╚══════╝╚═╝     ╚═╝    ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝
```

### 🔪 *A murder has been committed. Four suspects. One killer. Can you solve it?*

<br>

![Python](https://img.shields.io/badge/Python-3.10+-1a1610?style=for-the-badge&logo=python&logoColor=e8d5a3&labelColor=0d0b08)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-1a1610?style=for-the-badge&logo=streamlit&logoColor=e8d5a3&labelColor=0d0b08)
![LangChain](https://img.shields.io/badge/LangChain-AWS-1a1610?style=for-the-badge&logo=chainlink&logoColor=e8d5a3&labelColor=0d0b08)
![Amazon Bedrock](https://img.shields.io/badge/Amazon_Bedrock-Nova_Pro-1a1610?style=for-the-badge&logo=amazonaws&logoColor=e8d5a3&labelColor=0d0b08)

</div>

---

## 🕵️ What is this?

**LLM Detective** is an AI-powered murder mystery game built with Streamlit and Amazon Bedrock. Every game is unique — the AI generates a fresh case on demand: new setting, new victim, new suspects, new killer. You interrogate suspects, collect clues, and make your accusation. The AI plays *all* the characters and *never contradicts itself* thanks to LangChain memory.

> *"An empty bottle of Evelyn's favourite wine... in Gerald's study. That doesn't sound right."*  
> — Clara Thompson, suspect

---

## 📸 Screenshots

| Interrogation Room | Make Your Accusation |
|---|---|
| ![Interrogation](screenshots/output1.png) | ![Accusation](screenshots/output2.png) |

---

## ✨ Features

- 🎲 **Infinite unique mysteries** — AI generates a fresh case every time (setting, victim, 4 suspects, killer, motive, weapon)
- 🧠 **Persistent memory** — LangChain message history keeps the AI consistent across the entire game
- 🎭 **Full character acting** — the AI voices every suspect in-character, with personality and nervous tells
- 📋 **Detective's Notebook** — save clues from answers to your sidebar notebook as you play
- 🔒 **One-shot accusation** — name your killer, weapon, and motive. You only get one chance
- 🌑 **Noir UI** — dark, atmospheric design with Playfair Display typography

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Amazon Nova Pro via Amazon Bedrock |
| Memory & Chaining | LangChain (`langchain-aws`, `langchain-core`) |
| State Management | Streamlit `session_state` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- AWS account with Bedrock access (Amazon Nova Pro enabled)
- AWS credentials configured (`~/.aws/credentials` with a `default` profile)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/llm-detective.git
cd llm-detective

# 2. Install dependencies
pip install streamlit langchain-aws langchain-core

# 3. Run the game
streamlit run app.py
```

Then open `http://localhost:8501` in your browser and click **Begin New Investigation**.

---

## 📁 Project Structure

```
llm-detective/
│
├── app.py                 # Streamlit UI — all three game phases
├── chatbot_backend.py     # LLM logic — case generation, interrogation, accusation
├── game_state.py          # State helpers — clue notebook, chat log, phase tracking
├── screenshots/
│   ├── dec1.png
│   └── dec2.png
└── README.md
```

---

## 🎮 How to Play

```
1. Click "Begin New Investigation"
      ↓
   AI secretly generates: setting · victim · killer · weapon · motive · 4 suspects
      ↓
2. Select a suspect from the left panel
      ↓
3. Ask them questions — about their alibi, relationship with the victim, that night
      ↓
4. Save suspicious answers to your Detective's Notebook (sidebar)
      ↓
5. When ready → open "Make Your Accusation"
      ↓
6. Name the killer · weapon · motive → Submit
      ↓
   ✅ Correct → Full cinematic reveal
   ❌ Wrong   → One hint, game continues
```

---

## 💡 How It Works

The game uses **two separate AI calls**:

**1. Case Generation** — on "Begin New Investigation", the AI is prompted to generate a complete secret case file: suspects with true/false alibis, hidden secrets, physical clues, and a non-obvious killer. This is injected into the system prompt.

**2. Interrogation** — every question appends to a `LangChain` message list (the memory). The AI has the full case file in its system prompt and the full conversation history every time it responds — so it can never contradict what it said three questions ago.

```python
# The memory is just a list of LangChain messages
messages = memory + [HumanMessage(content=f"[Addressing {suspect}]: {question}")]
response = llm.invoke(messages)
memory.append(HumanMessage(...))
memory.append(AIMessage(...))
```

---

## 🔧 Configuration

To change the LLM model or region, edit `chatbot_backend.py`:

```python
def get_llm():
    return ChatBedrockConverse(
        credentials_profile_name='default',
        region_name="us-east-1",          # ← change region here
        model="us.amazon.nova-pro-v1:0",  # ← swap model here
        temperature=0.7,
        max_tokens=1000
    )
```

---

## 🗺️ Roadmap

- [ ] Difficulty levels (Easy = 6 questions min clues, Hard = no hints)
- [ ] Export solved case as a short story
- [ ] Multiplayer mode — two players interrogate simultaneously  
- [ ] Voice mode — TTS for each character
- [ ] Leaderboard — fewest questions to solve

---

## 🤝 Contributing

Pull requests welcome! Open an issue first for major changes.

---

## 📄 License

MIT — do whatever you want with it.

---

<div align="center">

*Built with ☕ and too many unresolved murder mysteries*

</div>
