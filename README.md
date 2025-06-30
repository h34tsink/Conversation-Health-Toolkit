# 🧠 Conversation Health Toolkit (CHT)

A toolkit for cultivating healthier, more constructive conversations—especially when using AI systems like ChatGPT. It addresses known weaknesses in AI chat behavior such as derailment, false balance, over-accommodation, and shallow engagement, using a structured and principled framework.

---

## ✨ What’s Included

- **`modular_prompt_kit.md`**  
  A living library of psychologically informed prompts and modules. Use it to steer conversations toward clarity, humility, empathy, and shared understanding.

- **`cht_validator.py`**  
  A Python script that automatically tests prompt effectiveness via the OpenAI API. It uses semantic similarity, keyword heuristics, and optional logging to learn which prompts pass or fail according to their intended principle.

- **`cht_prompt_cache.json`**  
  Automatically generated and updated by the validator. Caches test prompts, results, timestamps, pass/fail status, and feedback for iteration and learning.

- **`cht_dashboard_app.html`**  
  A local, offline dashboard. Load your cached JSON results to see pass/fail stats, semantic scores, feedback on failed prompts, and overall testing history in a readable format.

---

## 🧪 Usage

### 1. Generate & Validate Prompts

```bash
python cht_validator.py
```

This will:

- Use the CHT doc to generate principle-aligned prompts
- Send those prompts to GPT-4o via the OpenAI API
- Evaluate the output for alignment (semantics + keywords)
- Log results and feedback into `cht_prompt_cache.json`

### 2. Visualize Results

Open `cht_dashboard_app.html` in any browser and upload your JSON results. You’ll see:

- All tested principles
- Whether they passed or failed
- Scores and keyword hits
- GPT-generated explanations for any failed test

---

## 🎯 Why It Matters

AI often fails to:

- Respect ideological nuance
- Prevent derailed or ego-heavy conversations
- Balance emotional safety with informational clarity
- Recognize when a prompt undermines cognitive or conversational integrity

The CHT provides a solution: modular, tested interventions that real humans—or AI systems—can use to repair, redirect, or deepen the conversation.

---

## 🔧 Future Add-Ons

- Streamlit-powered analytics view
- Prompt regeneration & suggestion engine
- Integration with Obsidian or VS Code
- Batch topic testing from live discourse
