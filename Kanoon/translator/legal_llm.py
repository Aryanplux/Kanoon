# translator/legal_llm.py
import random
import json
import os
import re

from .legal_index import search_similar_documents

# Predefined legal response templates (kept short)
LEGAL_RESPONSES = {
    "contract": [
        "A contract requires offer, acceptance, and consideration.",
        "Both parties must voluntarily agree to the terms."
    ],
    "property": [
        "Property laws vary based on ownership type: joint, leasehold, freehold, etc."
    ],
    "employment": [
        "Employees have a right to a safe work environment and fair wages."
    ],
    "family": [
        "Family law covers marriage, divorce, child custody, and inheritance."
    ],
    "criminal": [
        "Criminal law: innocent until proven guilty. Legal representation is important."
    ],
    "civil": [
        "Civil law deals with disputes between individuals or organizations."
    ]
}

GENERAL_LEGAL_INFO = [
    "Always maintain proper documentation for legal matters.",
    "Understanding your rights is the first step in legal protection.",
    "Seek legal counsel for case-specific guidance."
]

def categorize_question(question: str) -> str:
    q = question.lower()
    if "contract" in q or "agreement" in q:
        return "contract"
    if "property" in q or "land" in q or "ownership" in q:
        return "property"
    if "job" in q or "employment" in q or "salary" in q:
        return "employment"
    if "divorce" in q or "custody" in q or "marriage" in q:
        return "family"
    if "crime" in q or "murder" in q or "theft" in q or "criminal" in q:
        return "criminal"
    if "sue" in q or "lawsuit" in q or "damages" in q:
        return "civil"
    return "general"

def ask_legal_llm(question: str) -> str:
    """
    Main entry point used by UI.
    It first looks for exact article/section matches in the structured DB,
    then keywords via FTS, then semantic similarity. Falls back to category templates.
    """
    try:
        if not question or not question.strip():
            return "Please provide a legal question for assistance."

        print(f"Processing legal question: {question}")
        category = categorize_question(question)
        print(f"Categorized as: {category}")

        response_parts = []
        response_parts.append(f"Regarding your question: \"{question}\"\n")

        # Try the structured DB (titles/sections) and similarity search
        matches = search_similar_documents(question, top_k=5)
        if matches:
            response_parts.append("Matched Legal References / Similar Documents:")
            response_parts.extend(f"• {m}" for m in matches[:5])
        else:
            # fallback to category responses
            if category in LEGAL_RESPONSES:
                response_parts.append("Here's some general information that might be relevant:")
                response_parts.extend(f"• {info}" for info in LEGAL_RESPONSES[category])
            else:
                response_parts.append("General legal insights:")
                response_parts.extend(f"• {info}" for info in random.sample(GENERAL_LEGAL_INFO, min(3, len(GENERAL_LEGAL_INFO))))

        # standard footer
        response_parts.append("\nGeneral recommendations:")
        response_parts.append("• Consult a qualified attorney for case-specific legal advice.")
        response_parts.append("• Research applicable laws in your jurisdiction.")
        response_parts.append("\n" + "="*50)
        response_parts.append("DISCLAIMER: This is general information only and not legal advice.")
        response_parts.append("="*50)

        return "\n".join(response_parts)

    except Exception as e:
        print("Error in legal_llm:", e)
        return "I encountered an internal error while processing your question."
