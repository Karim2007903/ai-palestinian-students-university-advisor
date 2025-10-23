# AI Palestine Student University Advisor (ReAct Agent)

**Attribution:**
This code is inspired by the AI Agents in LangGraph course by DeepLearning.AI, which itself builds on [Simon Willison's Python ReAct pattern](https://til.simonwillison.net/llms/python-react-pattern).

This project implements a ReAct (Reasoning and Acting) agent that acts as an intelligent advisor for Palestinian students seeking universities and scholarships worldwide. The agent combines reasoning and acting to analyse each student’s academic profile (grades, field of study, language proficiency, etc.) and uses real-time web search to provide accurate, current information about admission requirements, university rankings, available scholarships, and application deadlines.

## Project Structure
- `main.py`: Contains the complete implementation including:
  - `Agent` class for handling conversations
  - Action implementations (calculate, search)
  - Query processing and execution logic
  - Advisor prompt and guidance tailored to Palestinian students
- `requirements.txt`: Project dependencies
- `tests/`: Test cases directory

## Features
- **ReAct pattern implementation** (Reasoning and Acting)
- **Real-time web search** using Tavily for up-to-date admissions, scholarships, and deadlines
- **Scholarship discovery** (governmental, university, private foundations; need- and merit-based)
- **Qualification-aware evaluation** (Tawjihi, A-levels, IB, SAT, BTEC, and more)
- **Course and university recommendations** with entry requirements and ranking context
- **Application guidance** including language tests (IELTS/TOEFL), documents, and timelines
- **Conversation memory** and context management
- **Integration with OpenRouter** using `deepseek/deepseek-r1-0528-qwen3-8b:free`

## Available Actions
- `search`: Searches the web for admissions, scholarships, rankings, visa pages, and deadlines
  - Example: `search: "Computer Engineering scholarships for Palestinian students Germany 2026"`
- `calculate`: Performs calculations for grade averages, UCAS points, GPA conversions, or scholarship eligibility thresholds
  - Example: `calculate: (94 + 91 + 88) / 3` for an average from three course scores

## Setup
1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage
The main script includes an example query that demonstrates the agent's capabilities:

```python
from main import Agent, load_dotenv_and_init_client, query

# Initialise the OpenRouter and Tavily clients
load_dotenv_and_init_client()

# Create an agent instance
agent = Agent(prompt)  # prompt is defined in main.py

# Ask a question about universities and scholarships
question = (
    "I am a Palestinian student with Tawjihi 94% and IELTS 6.5, interested in "
    "Computer Engineering in Germany or Türkiye. What universities and scholarships should I consider?"
)
query(question, agent)
```

The agent will:
1. Process the student's academic background and interests (e.g., Tawjihi score, language level)
2. Search for current admissions information, scholarships, and deadlines
3. Calculate averages or convert grades when relevant
4. Provide specific university and scholarship recommendations
5. Offer actionable next steps and required documents

## Example Output
The agent provides comprehensive responses including:
- **University recommendations** with typical entry requirements and ranking context
- **Scholarship options** (eligibility, benefits, deadlines, links)
- **Language test guidance** (IELTS/TOEFL thresholds and preparation pointers)
- **Documentation checklist** (transcripts, passport, recommendation letters, personal statement)
- **Timelines and deadlines** tailored to target countries
- **Alternative pathways** (foundation years, community colleges, pathway providers) when appropriate

## Supported Queries
The agent can help with:
- Course and university recommendations by country/region
- Scholarship discovery for Palestinian students (global and country-specific)
- Entry requirement analysis (Tawjihi, A-levels, IB, SAT/ACT, GPA conversions)
- Language test requirements and preparation guidance
- Application strategy (deadlines, staged plans, safety/target/reach choices)
- University rankings and comparisons
- Fee estimates, living costs, and funding guidance
- Visa guidance links and official government/university resources

## API Requirements
- **OpenRouter API Key**: For accessing the DeepSeek model
- **Tavily API Key**: For real-time web search capabilities

Both services offer free tiers suitable for testing and development.

## Testing

You can run the test suite using pytest. Ensure dependencies are installed (pytest is included in `requirements.txt`).

1. Install dependencies (inside your virtual environment):
```bash
pip install -r requirements.txt
```

2. Run all tests (recommended):
```bash
python3 -m pytest -q
```

3. Run tests for a single file (this repository uses `test_main.py`):
```bash
python3 -m pytest -q test_main.py
```

4. See which tests ran, their names, and pass/fail status (recommended):
```bash
python3 -m pytest -vv
```

Note: To also see print output from tests, append `-s` (e.g., `python3 -m pytest -vv -s`).

Notes:
- The tests include logic to exercise the ReAct loop using mock agents and stubbed search calls, so no external API calls are made during testing.
- To run just a single test function, you can use the `-k` flag, for example:
```bash
python3 -m pytest -k test_query_flow_with_mock_agent_calculate -vv -s
```

## Suggested Improvements
This project is an MVP and there is plenty of room for improvement. Ideas for future contributors:
- Improve response speed and quality by using a stronger model and enabling streaming output
- Add more assertions and structured checks in tests; increase coverage
- Introduce retries and backoff for network calls; cache stable lookups; normalise citation formats
- Expand qualification handling (detailed Tawjihi equivalencies, country-specific grade conversions)
- Enhance the ReAct loop with stricter output validation and better error handling on missing observations
- Add configuration for target countries, fee status, and scholarship preferences; persist user profile between runs
- Provide a lightweight UI (CLI flags or simple web UI) for easier use; support Arabic output
- Add pre-commit hooks (formatting, linting, security/secret scans) and CI to run tests automatically
- Incorporate currency conversion and cost-of-living data with caching

This repository intentionally uses UK English throughout.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
