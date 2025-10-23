# AI Palestine Student University Advisor (ReAct Agent)

**Attribution:**
This code is based on materials from the AI Agents in LangGraph course by DeepLearning.AI, 
which itself is based on [Simon Willison's Python ReAct pattern](https://til.simonwillison.net/llms/python-react-pattern).

This project implements a ReAct (Reasoning and Acting) agent that acts as an expert University and Scholarship Advisor 
specialising in opportunities for **Palestinian students**.  
The agent combines reasoning and acting to help students find suitable universities, scholarships, and admission opportunities 
around the world using real-time web search capabilities.

This repository also serves as a lightweight, terminal-run version of my AI education advisory initiative, **Anyverse Palestine**.

## Project Structure
- `main.py`: Contains the complete implementation including:
  - `Agent` class for managing conversations
  - Action implementations (`calculate`, `search`)
  - Query processing and ReAct execution logic
  - University & scholarship advisor prompt and behavioural rules
- `requirements.txt`: Project dependencies
- `tests/`: Test cases directory

## Features
- **ReAct pattern implementation** (Reasoning and Acting)
- **Real-time web search** using Tavily for live data on scholarships and universities
- **GPA and UCAS equivalency calculations** for international admissions
- **Scholarship and course recommendations** based on eligibility
- **Admission guidance** and personalised improvement advice
- **Conversation memory** for multi-turn reasoning
- **Integration with OpenRouter** using `deepseek/deepseek-r1-0528-qwen3-8b:free` model

## Available Actions
- `search`: Searches the web for scholarships, university rankings, entry requirements, and application deadlines  
  - Example:  
    ```python
    search: "Scholarships for Palestinian students studying Computer Science in Europe 2026"
    ```
- `calculate`: Performs GPA or UCAS point calculations and other numerical analyses  
  - Example:  
    ```python
    calculate: (120 + 32 + 40)
    ```

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
The main script includes an example query that demonstrates the agent’s functionality:

```python
from main import Agent, load_dotenv_and_init_client, query

# Initialise the OpenRouter and Tavily clients
load_dotenv_and_init_client()

# Create an agent instance
agent = Agent(prompt)  # prompt is defined in main.py

# Ask a question about scholarships and universities
question = "I am a Palestinian student with a 94% average and IELTS 7.5. What Computer Science scholarships and universities can I apply to in the UK or Europe?"
query(question, agent)
```

The agent will:
1. Process the student’s academic profile and interests  
2. Search for current scholarship and university opportunities  
3. Calculate GPA/UCAS equivalencies and assess eligibility  
4. Provide specific recommendations with deadlines and links  
5. Offer personalised guidance for application improvement  

## Example Output
The agent provides comprehensive results including:
- **Scholarship recommendations** (Chevening, Erasmus+, Türkiye Scholarships, HESP, etc.)
- **University suggestions** (University of Glasgow, TU Delft, Bilkent University)
- **Eligibility analysis** (based on GPA, IELTS, and requirements)
- **Application advice** (personal statement focus areas)
- **Important deadlines** and direct links to apply

## Supported Queries
The agent can assist with:
- Scholarship search and eligibility checks
- University and program recommendations
- GPA to UCAS point conversions
- Application strategy advice
- Admission and language requirement lookups
- University rankings and global comparisons
- Important scholarship and university deadlines

## API Requirements
- **OpenRouter API Key**: For accessing the DeepSeek reasoning model  
- **Tavily API Key**: For real-time web search functionality  

Both services offer free tiers suitable for testing and early development (I know — I built this while broke too).

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

3. Run tests for a single file:
```bash
python3 -m pytest -q test_main.py
```

4. See detailed test names and pass/fail status:
```bash
python3 -m pytest -vv
```

To see print output from tests, append `-s` (e.g., `python3 -m pytest -vv -s`).

Notes:
- The tests simulate the ReAct reasoning loop using mock agents and stubbed search results (no live API calls).
- To run a specific test function, use the `-k` flag, for example:
```bash
python3 -m pytest -k test_query_flow_with_mock_agent_calculate -vv -s
```

## Suggested Improvements

This project is an MVP built with a free model, so responses may be slow and limited.  
Future contributors are encouraged to:
- Improve response quality and latency using stronger models
- Expand qualification handling (Tawjihi, IB, SAT, BTEC, etc.)
- Add retries and caching for search results
- Include structured output validation and better error handling
- Add configurable options (country, subject, year of entry)
- Build a simple UI for web or CLI access
- Increase test coverage and add CI/CD automation
- Introduce PDF export for scholarship reports

This repository intentionally uses **international English** throughout.

## Project Idea
The **AI Palestine Student University Advisor** is an intelligent ReAct-based agent designed to help Palestinian students find suitable **universities and scholarships** around the world.  
It analyses each student’s academic background and uses **real-time web search** to deliver accurate, up-to-date information about **admission requirements, rankings, and application deadlines**.  
The goal is to provide an AI-powered virtual advisor that makes global education **accessible, free, and personalised** for Palestinian students.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
```
