from flask import Flask, render_template, request
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# LLM
llm = ChatOpenAI(
    model="gpt-5-nano"
)

# Agent
agent = Agent(
    role="AI Assistant",
    goal="Answer user questions clearly",
    backstory="You are a helpful AI assistant.",
    llm=llm,
    verbose=False
)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""

    if request.method == "POST":
        question = request.form["question"]

        task = Task(
            description=f"Answer this question clearly: {question}",
            expected_output="Clear helpful answer.",
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )

        result = crew.kickoff()
        answer = result

    return render_template("index.html", answer=answer, question=question)


if __name__ == "__main__":
    app.run(debug=True)