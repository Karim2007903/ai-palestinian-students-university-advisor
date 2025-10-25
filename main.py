(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/main.py b/main.py
--- a/main.py
+++ b/main.py
@@ -0,0 +1,400 @@
+import os
+import re
+import json
+from dotenv import load_dotenv
+from openai import OpenAI
+from tavily import TavilyClient
+
+# Global OpenRouter client
+client = None
+# Global Tavily client
+tavily_client = None
+
+
+def search_tavily(query: str):
+    """Search using Tavily; requires prior initialisation via load_dotenv_and_init_client."""
+    if tavily_client is None:
+        raise Exception(
+            "Tavily client not initialised. Call load_dotenv_and_init_client() first."
+        )
+    response = tavily_client.search(query)
+    return response
+
+
+class Agent:
+    """Simple chat agent with optional system prompt and model selection."""
+
+    def __init__(self, system: str = "", model: str = "deepseek/deepseek-r1-0528-qwen3-8b:free"):
+        self.system = system
+        self.model = model
+        self.messages = []
+        if self.system:
+            self.messages.append({"role": "system", "content": system})
+
+    def save_history(self, filename: str = "history.json") -> None:
+        with open(filename, "w") as f:
+            json.dump(self.messages, f)
+
+    def load_history(self, filename: str = "history.json") -> None:
+        try:
+            with open(filename, "r") as f:
+                self.messages = json.load(f)
+        except FileNotFoundError:
+            pass
+
+    def __call__(self, message: str) -> str:
+        self.messages.append({"role": "user", "content": message})
+        result = self.execute()
+        self.messages.append({"role": "assistant", "content": result})
+        return result
+
+    def execute(self) -> str:
+        if client is None:
+            raise Exception(
+                "OpenRouter client not initialised. Call load_dotenv_and_init_client() first."
+            )
+
+        # For Gemma-family models, prepend system to first user message
+        if "gemma" in self.model.lower():
+            messages = self.messages.copy()
+            system_msg = None
+            if messages and messages[0]["role"] == "system":
+                system_msg = messages.pop(0)
+            if messages and messages[0]["role"] == "user" and system_msg is not None:
+                messages[0]["content"] = (
+                    f"SYSTEM: {system_msg['content']}\n\nUSER: {messages[0]['content']}"
+                )
+            completion = client.chat.completions.create(
+                model=self.model, temperature=0.2, messages=messages
+            )
+        else:
+            completion = client.chat.completions.create(
+                model=self.model, temperature=0.2, messages=self.messages
+            )
+
+        return completion.choices[0].message.content
+
+
+prompt = """
+You are an AI Palestine Students University Advisor focused on helping Palestinian students discover suitable degree programs and scholarships worldwide. Use UK English. Your goal is to provide accurate, up-to-date information for the student's intended intake (default to 2026 unless specified), covering admissions, language requirements, tuition/fees, living costs notes, and scholarship opportunities.
+
+You operate in a strict ReAct loop with this output contract:
+- When taking an action, output ONLY:
+  Thought: <your brief reasoning>
+  Action: <one of the allowed actions below>
+  PAUSE
+- When you have enough information to respond to the user, output ONLY:
+  Answer: <your final answer to the user>
+Do not include both action and answer in the same turn. Do not output anything other than the fields shown above.
+
+Available actions:
+- search: Search the web for current program information (e.g., fees, modules), official university pages, typical entry requirements, scholarship information, and deadlines.
+  Example:
+  Action: search: "full scholarships for Palestinian students Computer Science 2026 site:*.ac.uk OR site:*.edu"
+- calculate: Perform calculations for grade/GPA mappings, averages, UCAS points (if relevant), budgets, or other numerical assessments.
+  Example:
+  Action: calculate: (48 + 40 + 32)
+
+Before searching, if key inputs are missing, ask concise clarifying questions (in an Answer turn). Ask about:
+- Subject/area of interest; current/previous qualifications (e.g., Tawjihi percentage/GPA, A levels/IB/BTEC), achieved or predicted grades
+- Year of entry; target countries/regions; budget/fee status; visa needs; language proficiency (IELTS/TOEFL/DUOLINGO)
+- Interests (e.g., AI, data science), course type (with placement/abroad), and flexibility about foundation years or pathway colleges
+
+UCAS tariff (A levels, 2017+ scale):
+- A* = 56, A = 48, B = 40, C = 32, D = 24, E = 16
+When relevant, calculate UCAS points explicitly and state the formula. If the student uses other qualifications (IB, BTEC, Scottish Highers, Tawjihi, SATs, etc.), prefer searching for official equivalencies and cite sources.
+
+Scholarships and funding guidance:
+- Prioritise official university scholarships, government/embassy schemes, major external awards (e.g., Chevening, DAAD, Türkiye Scholarships), and Palestinian-eligible opportunities
+- Clearly indicate eligibility, coverage (tuition/stipend/fees), and key dates; if data varies or is unclear, say so and link to official pages
+
+Source quality and citations:
+- Prefer official sources: university pages (*.ac.uk/*.edu), official policy pages, UCAS (when applicable), and recognised league tables (CUG, Guardian, Times/Sunday Times, QS)
+- Include 2–4 citations in your Answer when data depends on current info. Format:
+  - <Title> — <URL> (Accessed: <Month YYYY>)
+- If a specific figure/date is unknown or varies, say so and direct the user to the official source.
+
+Formatting for Answer:
+- Start with a short summary tailored to the student (qualifications, target regions, constraints)
+- Provide 3–6 specific program recommendations with entry requirements and any scholarship notes
+- When helpful, include a compact table (University | Course | Typical Entry | Notes)
+- Mention application timelines (e.g., EU/UK main cycles, priority scholarship windows, country-specific intakes)
+- Give actionable next steps (tests to take, documents to prepare, items to verify on official pages)
+- If you suggest more than 5 courses, make it clear that many central application portals cap application counts (e.g., UCAS at 5)
+
+Error handling:
+- If search returns low/no results, say what was attempted and suggest improved queries or broader criteria
+- If sources conflict, explain the discrepancy and prefer the most official/authoritative page
+
+Example session:
+
+Question: I have 95% in Tawjihi (Scientific stream) and IELTS 7.0. I want Computer Science programs in Europe or Turkey with scholarship options. What should I consider for Fall 2026?
+
+Thought: Confirm typical thresholds and then search for CS entry requirements and scholarship programmes.
+Action: search: "site:*.edu OR site:*.ac.uk Computer Science entry requirements 2026 IELTS 6.5 7.0"
+PAUSE
+
+Observation: [Search results about Computer Science entry requirements and related scholarships]
+
+Answer: Based on your profile (Tawjihi 95% ≈ competitive for many programmes; IELTS 7.0 meets typical 6.0–6.5 bands), consider:
+- <University> — BSc Computer Science (Typical entry high school certificate with strong maths; English IELTS 6.5). Explore merit scholarships.
+- <University> — BSc CS with AI (Higher threshold; check scholarship deadlines). Stretch option.
+Next steps:
+- Shortlist 4–6 programmes and verify their 2026 requirements on official pages.
+- Prepare statements and references; check priority scholarship windows.
+- Confirm language and document requirements; align with visa timelines.
+
+Citations:
+- <Title> — <URL> (Accessed: <Month YYYY>)
+- <Title> — <URL> (Accessed: <Month YYYY>)
+
+Summary of guidelines for your responses:
+- Always search for current, up-to-date information.
+- If you do not know a specific figure (e.g., deposit amount), say you do not know or direct the user to the official page.
+- Do not make up or guess specific fees, dates, or requirements.
+- Provide specific programme and scholarship recommendations with entry thresholds when possible.
+- Calculate UCAS points when relevant; for other systems, prefer official equivalence references.
+- Mention application deadlines and important dates when found.
+- Suggest alternative courses or pathways when appropriate (e.g., foundation or pathway colleges).
+
+If the user asks about something unrelated to university admissions, respond:
+Answer: Sorry, I can't answer that. As an AI University Application Advisor, I am designed to assist with higher education applications and related academic guidance.
+""".strip()
+
+
+def safe_calculate(expression: str):
+    """Safely evaluate mathematical expressions without using eval().
+
+    Supports +, -, *, / and parentheses. Accepts numbers with optional comma
+    thousands separators, which are removed before parsing.
+    """
+    try:
+        if expression is None:
+            raise ValueError("Empty expression")
+        # Normalize whitespace and remove thousands separators
+        expression = expression.strip()
+        expression_no_commas = expression.replace(",", "")
+
+        # Disallow obviously dangerous characters
+        dangerous_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_[]{}|\\`~@#$%^")
+        if any(c in dangerous_chars for c in expression_no_commas):
+            raise ValueError("Expression contains potentially dangerous characters")
+
+        # Allow only safe characters
+        safe_chars = set("0123456789+-*/(). ")
+        if not all(c in safe_chars for c in expression_no_commas):
+            other_chars = set(expression_no_commas) - safe_chars
+            if any(c in dangerous_chars for c in other_chars):
+                raise ValueError("Expression contains potentially dangerous characters")
+
+        # Delegate to parser
+        if "(" in expression_no_commas or ")" in expression_no_commas:
+            return evaluate_expression(expression_no_commas)
+        return evaluate_simple_expression(expression_no_commas)
+    except Exception as e:
+        return f"Error calculating: {str(e)}"
+
+
+def evaluate_simple_expression(expr: str) -> float:
+    """Evaluate simple arithmetic expressions without parentheses."""
+    parts = re.split(r"([+\-*/])", expr.replace(" ", ""))
+    parts = [p for p in parts if p]
+
+    if len(parts) == 1:
+        return float(parts[0])
+
+    # Handle multiplication and division first
+    i = 1
+    while i < len(parts) - 1:
+        if parts[i] in ["*", "/"]:
+            left = float(parts[i - 1])
+            right = float(parts[i + 1])
+            if parts[i] == "*":
+                result = left * right
+            else:
+                if right == 0:
+                    raise ValueError("Division by zero")
+                result = left / right
+            parts[i - 1 : i + 2] = [str(result)]
+            i -= 1
+        i += 2
+
+    # Handle addition and subtraction
+    result = float(parts[0])
+    for i in range(1, len(parts), 2):
+        if i + 1 < len(parts):
+            if parts[i] == "+":
+                result += float(parts[i + 1])
+            elif parts[i] == "-":
+                result -= float(parts[i + 1])
+
+    return result
+
+
+def evaluate_expression(expr: str) -> float:
+    """Evaluate expressions with parentheses by reducing innermost pairs first."""
+    while "(" in expr:
+        start = expr.rfind("(")
+        end = expr.find(")", start)
+        if end == -1:
+            raise ValueError("Mismatched parentheses")
+        inner_expr = expr[start + 1 : end]
+        inner_result = evaluate_simple_expression(inner_expr)
+        expr = expr[:start] + str(inner_result) + expr[end + 1 :]
+    return evaluate_simple_expression(expr)
+
+
+# Create a dictionary of known actions
+known_actions = {"calculate": safe_calculate, "search": search_tavily}
+
+# Action regex: e.g., "Action: search: something"
+action_re = re.compile(r"^Action: (\w+): (.*)$")
+
+
+def query(question: str, agent: Agent, max_turns: int = 5) -> None:
+    print(f"Question: {question}\n")
+    next_prompt = question
+    for i in range(max_turns):
+        result = agent(next_prompt)
+        agent.save_history()
+        print(f"--- Turn {i + 1} ---")
+        print(result)
+        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
+        if actions:
+            action, action_input = actions[0].groups()
+            if action not in known_actions:
+                print(f"Unknown action: {action}: {action_input}")
+                return
+            print(f"Action: {action}('{action_input}')")
+            observation = known_actions[action](action_input)
+            print(f"Observation: {observation}\n")
+            next_prompt = f"Observation: {observation}"
+        else:
+            if result.startswith("Answer:"):
+                print(f"\nFinal Answer: {result.split('Answer: ', 1)[1]}")
+            else:
+                print("No action taken and no clear answer. Stopping.")
+            return
+    print("Max turns reached.")
+
+
+def load_dotenv_and_init_client() -> None:
+    global client, tavily_client
+    _ = load_dotenv()
+    api_key = os.getenv("OPENROUTER_API_KEY")
+    tavily_api_key = os.getenv("TAVILY_API_KEY")
+
+    if not api_key:
+        raise ValueError(
+            "OPENROUTER_API_KEY not found in .env file or environment variables."
+        )
+    if not tavily_api_key:
+        raise ValueError(
+            "TAVILY_API_KEY not found in .env file or environment variables."
+        )
+
+    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
+    tavily_client = TavilyClient(tavily_api_key)
+
+
+def is_question(user_input: str) -> bool:
+    question_words = [
+        "who",
+        "what",
+        "when",
+        "where",
+        "why",
+        "how",
+        "which",
+        "can",
+        "is",
+        "are",
+        "do",
+        "does",
+        "did",
+        "will",
+        "could",
+        "would",
+        "should",
+    ]
+    input_lower = user_input.lower().strip()
+    for word in question_words:
+        if re.search(rf"\\b{word}\\b", input_lower):
+            return True
+    non_questions = ["i have no more questions", "that's all", "no more questions"]
+    for statement in non_questions:
+        if input_lower.startswith(statement) and input_lower.endswith("?"):
+            return False
+    if input_lower.endswith("?"):
+        return True
+    return False
+
+
+def get_ucas_points(grade: str, subject_type: str = "A-level") -> int:
+    """Get UCAS points for a given grade and subject type."""
+    ucas_points = {
+        "A-level": {"A*": 56, "A": 48, "B": 40, "C": 32, "D": 24, "E": 16},
+        "AS-level": {"A": 20, "B": 16, "C": 12, "D": 10, "E": 6},
+        "BTEC": {"D*": 56, "D": 48, "M": 32, "P": 16},
+    }
+    try:
+        return ucas_points.get(subject_type, {}).get(grade.upper(), 0)
+    except Exception:
+        return 0
+
+
+def calculate_ucas_total(grades_input: str) -> str:
+    """Calculate total UCAS points from a comma-separated list of '<Subject> <Grade>' entries."""
+    try:
+        grades = [g.strip() for g in grades_input.split(",")]
+        total = 0
+        breakdown = []
+        for grade_entry in grades:
+            if " " in grade_entry:
+                subject, grade = grade_entry.rsplit(" ", 1)
+                points = get_ucas_points(grade)
+                total += points
+                breakdown.append(f"{subject}: {grade} = {points} points")
+        result = f"Total UCAS points: {total}\nBreakdown:\n" + "\n".join(breakdown)
+        return result
+    except Exception as e:
+        return f"Error calculating UCAS points: {str(e)}"
+
+
+if __name__ == "__main__":
+    try:
+        load_dotenv_and_init_client()
+    except Exception as e:
+        print(f"Warning: client initialisation failed — {e}")
+    agent_instance = Agent(prompt)
+    try:
+        agent_instance.load_history()
+    except Exception:
+        pass
+
+    print("Welcome! I'm your AI Palestine Student University Advisor.")
+    print(
+        "Ask me anything related to universities, admissions, or scholarships. (Write 'exit' to exit. If you don't type a question, I'll end the conversation.)"
+    )
+
+    while True:
+        try:
+            user_input = input("\nAsk a question:\n> ").strip()
+        except (EOFError, KeyboardInterrupt):
+            print("\nGoodbye!")
+            break
+        if user_input.lower() == "exit":
+            print("Goodbye!")
+            break
+        if not user_input:
+            print("It looks like you have no questions for now. Goodbye.")
+            break
+        if is_question(user_input):
+            try:
+                query(user_input, agent_instance)
+            except Exception as e:
+                print(f"Error during query: {e}")
+        else:
+            print("It looks like you have no questions for now. Goodbye.")
+            break
+
EOF
)
