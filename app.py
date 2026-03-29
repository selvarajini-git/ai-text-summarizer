from flask import Flask, request, render_template_string
from transformers import pipeline

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Text Summarizer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        textarea {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .summary {
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Text Summarizer</h1>
        <form method="post">
            <textarea name="text" rows="6" placeholder="Enter your text here..."></textarea>
            <button type="submit">Summarize</button>
        </form>
        {% if summary %}
        <div class="summary">
            <h3>Summary:</h3>
            <p>{{ summary }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

print("Loading AI model... This may take a few minutes on first run")
generator = pipeline("text-generation", model="ibm-granite/granite-3.0-2b-instruct")
print("Model ready!")

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"Summarize this text: {text}"
        output = generator(prompt, max_length=80)
        summary = output[0]["generated_text"]
    return render_template_string(HTML_TEMPLATE, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
