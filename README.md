<li>To launch the simple chatbot answers with fastapi:</li>

into the llm directory

activate the virtualenv:
source llm_env/bin/activate

launching app:
uvicorn specializing:app --host 0.0.0.0 --port 8000 --reload 

<li>Using llm with pdf</li>
<p>The demo_2.py is the streamlit app associated with the specialized_with_rag.py llm api.</p>
<p>The latter uses the possibility to addition pdf data</p>
<p>First uvicorn specialized_with_rag:app --reload --port 8006 which might take a long time</p>
<p>Then streamlit run demo_2.py after fastapi is ready</p>
