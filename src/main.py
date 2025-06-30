# Functional CHT Validator using ChatGPT API
# Requires: openai, python-dotenv, scikit-learn, numpy, tiktoken (for semantic scoring)

from openai import OpenAI
import os
from datetime import datetime
import csv
import json
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 🔧 Core principles and expected outcomes
core_principles = {
    "Coherent Extrapolated Volition (CEV) Lens": "shared values",
    "Intellectual Humility": "uncertainty",
    "Moral Reframing": "fairness",
    "Diversity-of-Input": "source",
    "Self-Distancing & Future-View": "she thinks",
    "Boundary & Gray-Rock Moves": "time",
    "Cognitive-Load Management": "succinct",
    "Active-Listening Loops": "you feel",
    "Prosocial Framing": "cooperation",
    "Growth-Mindset Orientation": "learn"
}

# Load or create prompt cache
CACHE_FILE = "cht_prompt_cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        prompt_cache = json.load(f)
else:
    prompt_cache = {}

# Save prompt cache


def save_prompt_cache():
    def safe(obj):
        if isinstance(obj, bool):
            return str(obj)
        return obj
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(prompt_cache, f, indent=2, default=safe)

# 🧪 Dynamically generate prompts by asking GPT


def generate_tests():
    tests = []
    for principle, expected in core_principles.items():
        try:
            if principle in prompt_cache:
                prompt = prompt_cache[principle]["prompt"]
            else:
                system_msg = f"You are a prompt engineer. Generate a single user prompt that is detailed, concise, and removes ambiguity. The prompt should trigger a response illustrating the CHT principle '{principle}'."
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_msg}
                    ]
                )
                prompt = completion.choices[0].message.content.strip()
                prompt_cache[principle] = {"prompt": prompt, "history": []}
                save_prompt_cache()
            tests.append(
                {"name": principle, "prompt": prompt, "expect": expected})
        except Exception as e:
            print(f"Prompt generation error for {principle}: {e}")
    return tests

# 🧠 Semantic evaluation using embeddings


def semantic_similarity(a, b):
    try:
        a_embed = client.embeddings.create(
            input=[a], model="text-embedding-3-small").data[0].embedding
        b_embed = client.embeddings.create(
            input=[b], model="text-embedding-3-small").data[0].embedding
        return cosine_similarity([a_embed], [b_embed])[0][0]
    except Exception as e:
        print(f"Embedding error: {e}")
        return 0.0

# 💡 Enhanced evaluation: both keyword and semantic match


def evaluate_response(response, expected_keyword):
    semantic_target = {
        "shared values": "long-term agreement",
        "uncertainty": "acknowledging unknowns",
        "fairness": "moral equality",
        "source": "multiple perspectives",
        "she thinks": "third person reflection",
        "time": "sharing limits",
        "succinct": "concise explanation",
        "you feel": "emotional reflection",
        "cooperation": "working together",
        "learn": "growth from challenge"
    }.get(expected_keyword, expected_keyword)

    sim_score = semantic_similarity(response, semantic_target)
    keyword_pass = expected_keyword.lower() in response.lower()
    return keyword_pass or sim_score > 0.75, sim_score, keyword_pass

# 📝 Log results to CSV and JSON cache


def log_result(test_name, prompt, response, passed, sim_score, keyword_hit):
    with open("cht_test_results.csv", mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), test_name, prompt,
                        response[:300], passed, sim_score, keyword_hit])

    if test_name in prompt_cache:
        prompt_cache[test_name]["history"].append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "passed": str(passed),
            "score": sim_score,
            "keyword": keyword_hit,
            "sample": response[:300],
            "feedback": generate_failure_explanation(test_name, prompt, response, passed, sim_score, keyword_hit) if not passed else ""
        })
        save_prompt_cache()

# 🧾 Generate context-aware explanation when test fails


def generate_failure_explanation(name, prompt, response, passed, score, keyword):
    try:
        analysis_prompt = f"You are analyzing test output against the Conversation Health Toolkit. The failed test is for the principle: '{name}'.\n\nPROMPT:\n{prompt}\n\nRESPONSE:\n{response[:300]}\n\nSIMILARITY SCORE: {score}\nKEYWORD FOUND: {keyword}\n\nExplain why this response likely failed, and suggest a new prompt that better fits the principle."
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                    "content": "You are a helpful analyst trained on the CHT document."},
                {"role": "user", "content": analysis_prompt}
            ]
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating failure explanation: {e}"

# 🚀 Run each test


def run_tests():
    print("\n🔬 Running Functional CHT Tests via OpenAI API...\n")
    tests = generate_tests()
    for test in tests:
        print(f"🧪 {test['name']}")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a conversation facilitator applying a psychological module."},
                    {"role": "user", "content": test["prompt"]}
                ]
            )
            output = response.choices[0].message.content
            passed, sim_score, keyword_hit = evaluate_response(
                output, test["expect"])
            log_result(test["name"], test["prompt"], output,
                       passed, sim_score, keyword_hit)

            print(f"   ✅ Test Passed: {passed}")
            print(f"   🗣️ Output: {output[:200].strip()}...\n")

        except Exception as e:
            print(f"   ❌ API error: {e}\n")


if __name__ == "__main__":
    run_tests()
