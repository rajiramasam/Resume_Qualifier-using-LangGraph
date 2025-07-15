from flask import Flask, request, render_template
from graph_builder import build_graph
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
graph = build_graph()

def extract_text(file):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    else:
        return file.read().decode("utf-8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["resume"]
    resume_text = extract_text(file)
    result = graph.invoke({"resume": resume_text})
    return render_template("result.html", qualified=result["qualified"], message=result["message"])

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)