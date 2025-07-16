import google.generativeai as genai
from fastapi import HTTPException, status
from typing import Dict
from pathlib import Path


def build_prompt(question: str, log_text: str) -> str:
    return (
        f"""
        You are a cyber forensics expert in log analysis. Analyze system/network/application logs to detect malicious activity. An "attack" is any behavior from a source IP/entity attempting unauthorized access, disruption, or exploitation—like a hacker would.
        You'll be given:
        - A Hunter's (analyst’s) question
        - A log snippet (.log, .json, .txt, or SARIF)

        The hunter asks:
        {question}

        Here is the log data:
        {log_text}

        Please respond using the following format:

        🔍 Insights  
        🧠 Reasoning  
        📄 Supporting Logs: Line number, log line, interesting part of log  
        🛠️ Fixes or security measures that can be employed to prevent such attacks.
        """
    )


def call_gemini(log_file_path: Path, question: str, user) -> Dict[str, str]:
    if not user or not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated.")

    if not user.gemini_api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gemini API key is not set.")

    try:
        log_text = log_file_path.read_text(encoding='utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read log file: {str(e)}")

    prompt = build_prompt(question, log_text)

    try:
        genai.configure(api_key=user.gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt, stream=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API request failed: {str(e)}")

    raw_text = response.text if hasattr(response, "text") else ""

    return extract_sections(raw_text)


def extract_sections(response_text: str) -> Dict[str, str]:
    sections = {
        "insights": "",
        "reasoning": "",
        "supporting_logs": "",
        "fixes": ""
    }

    current_key = None
    for line in response_text.splitlines():
        striped_line = line.strip()

        if striped_line.startswith("🔍"):
            current_key = "insights"
            continue
        elif striped_line.startswith("🧠"):
            current_key = "reasoning"
            continue
        elif striped_line.startswith("📄"):
            current_key = "supporting_logs"
            continue
        elif striped_line.startswith("🛠️"):
            current_key = "fixes"
            continue

        if current_key:
            sections[current_key] += striped_line + "\n"

    return {k: v.strip() for k, v in sections.items()}
