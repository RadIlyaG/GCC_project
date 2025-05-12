#### ✅ How to distribute the entire project to other machines
Recommended approach: with dependency installation:

1. Save the required packages:
<br>pip freeze > requirements.txt

2. Share the project folder (excluding .venv) in this structure:
<br>GCC_Project/<br>
├── qsfc/<br>
│   └── PrepareOpenGraphs.py<br>
├── utils/<br>
│   └── lib_gen.py<br>
├── db.db<br>
├── requirements.txt

3. On the target machine:
- Navigate to the project folder:<br>
cd GCC_Project<br>
- Create a virtual environment:<br>
python -m venv .venv
- Activate it:<br>
.\\.venv\Scripts\activate
- install required packages:<br>
pip install -r requirements.txt

#### ✅ How to create a desktop shortcut
Right-click on your desktop → New → Shortcut
<br>Enter the following as the target:
<br>*Target:* C:\MyDocuments\ate\AutoTesters\Tools\GCC_Project\.venv\Scripts\python.exe c:/MyDocuments/ate/AutoTesters/Tools/GCC_Project/qsfc/PrepareOpenGraphs.py

*Give the shortcut a name like Run GCC Prepare*

*IMPORTANT:* This shortcut only works if the .venv already exists.

