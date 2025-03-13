import google.generativeai as genai
import os
import json
import re

# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyDvT0SWsLLVxZz_isAtAxM6xff3BHdXLCc"
genai.configure(api_key=GEMINI_API_KEY)

def generate_analogy():
    prompt = """
    You are an analogy creation assistant. Create ONE incomplete analogy with FOUR multiple-choice options.
    
    Requirements:
    1. Create a clear, educational english based (grammer) analogy with a missing element
    2. Provide four distinct answer options (A, B, C, D)
    3. Exactly ONE option should be the correct answer
    4. The difficulty should be moderate - challenging but solvable
    
    Return your response in valid JSON format as follows:
    {
      "analogy": "Your incomplete analogy here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 0
    }
    
    Note: The correct_index must be 0, 1, 2, or 3, corresponding to the position of the correct answer in the options array.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Extract JSON from response text
        response_text = response.text
        
        # Look for JSON pattern in the response
        json_match = re.search(r'({[\s\S]*})', response_text)
        if json_match:
            json_str = json_match.group(1)
            # Parse the JSON
            analogy_data = json.loads(json_str)
        else:
            # If no JSON pattern found, try parsing the whole response
            analogy_data = json.loads(response_text)

        # Ensure correct answer is accessible
        analogy_data["correct_answer"] = analogy_data["options"][analogy_data["correct_index"]]

        return analogy_data
    except Exception as e:
        print("Error:", e)
        # Fallback analogy in case of API failure
        return {
            "analogy": "Water is to ocean as sand is to _____.",
            "options": ["Mountain", "Desert", "River", "Forest"],
            "correct_index": 1,
            "correct_answer": "Desert"
        }

def evaluate_relevance(user_response, analogy):
    """
    Uses LLM to evaluate how relevant the user's response is to the given analogy.
    Returns a relevance score (0 to 10).
    """
    prompt =f"""
    You are an educational assessment expert. Evaluate how relevant this user response is to the given analogy.
    
    User response: "{user_response}"
    Analogy: "{analogy}"
    
    Instructions:
    1. Consider the conceptual relationship in the analogy
    2. Assess how well the user's response demonstrates understanding
    3. Assign a score from 0 to 10 where:
       - 0: Completely irrelevant/incorrect
       - 5: Partially relevant/correct
       - 10: Perfectly relevant/correct
    
    Return ONLY a number between 0 and 10 representing your score. Do not include any other text.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Try to get a clean number from the response
        score_text = response.text.strip()
        # Extract digits
        score_match = re.search(r'\b(\d+)\b', score_text)
        if score_match:
            score = int(score_match.group(1))
            return min(max(score, 0), 10)  # Ensure score is between 0 and 10
        else:
            # If no number found, try to parse JSON
            try:
                relevance_data = json.loads(score_text)
                return relevance_data.get("score", 5)  # Default to 5 if no score
            except:
                return 5  # Default score if parsing fails
    except Exception as e:
        print("Relevance evaluation error:", e)
        return 5  # Default to middle score if evaluation fails
