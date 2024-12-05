import os

def langsmith(_project_name=None):
    os.environ["LANGCHAIN_ENDPOINT"] = ("https://api.smith.langchain.com")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = _project_name