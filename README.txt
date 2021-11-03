After First time clone:
(Windows)
1. Open CMD with Admin Rights.
2. Use "cd" to navigate to project folder. (Google how to navigate with CMD if you don't know).
3. Enter "py -3 -m venv venv" (without quotes) to create virtual environment (venv).
4. Enter "venv\Scripts\activate" (without quotes) to activate the virtual environment.
5. Enter "set FLASK_APP=app.py" (without quotes) to set the app.py
6. Enter "pip install -r requirements.txt" (without quotes) to install all the modules required for the environment to run.
7. You should be good to go now.

(macOS/Linux)
1. Open Terminal.
2. Use "cd" to navigate to project folder. (Google how to navigate with CMD if you don't know).
3. Enter "python3 -m venv venv" (without quotes) to create virtual environment (venv).
4. Enter ". venv/bin/activate" (without quotes) to activate the virtual environment.
5. Enter "export FLASK_APP=app.py" (wihout quotes) to set the app.py
6. Enter "pip install -r requirements.txt" (without quotes) to install all the modules required for the environment to run.
7. You should be good to go now.


IMPORTANT:
Whenever you install a new module into your Flask virtual environment (venv). Make sure to use "pip freeze > requirements.txt" (without quotes) to create
a requirements.txt so other team members can install the correct modules for their environment.

Credit: Zichen901