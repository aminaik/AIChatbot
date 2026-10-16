# AI chatbot test practice

Setup:
    pip install -r requirements.txt
    playwright install

Run (the demo app starts automatically):
    python3 -m pytest -q
    python3 -m pytest -q -m safety          # one category
    python3 -m pytest -q --headed --slowmo 400

Expected result: everything passes, and 1 test is reported as "xfailed"
(BUG-101, the prompt-injection leak in app.py). To "fix" it, edit bot_reply()
in app.py; strict xfail will then flag the test as XPASS so you remove the marker.

Swap bot_reply() in app.py for a real LLM API call when you want to practice
against genuinely non-deterministic output.
