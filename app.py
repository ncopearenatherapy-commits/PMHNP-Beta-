import streamlit as st
import random
from questions import questions
import plotly.graph_objects as go

def render_mastery_donut(label, value):
    percent = int(value * 100)

    fig = go.Figure(
        data=[
            go.Pie(
                values=[percent, 100 - percent],
                hole=0.75,
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=["#3b82f6", "#e5e7eb"],
                    line=dict(color="white", width=2)
                ),
            )
        ]
    )

    fig.update_layout(
        height=180,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{percent}%</b><br>{label}",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_progress_donut(correct, total):
    percent = int((correct / total) * 100) if total > 0 else 0

    fig = go.Figure(
        data=[
            go.Pie(
                values=[percent, 100 - percent],
                hole=0.75,
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=["#6366f1", "#e5e7eb"],
                    line=dict(color="white", width=2)
                ),
            )
        ]
    )

    fig.update_layout(
        height=180,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{percent}%</b><br>Progress",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_performance_donut(label, correct, total):
    percent = int((correct / total) * 100) if total > 0 else 0

    fig = go.Figure(
        data=[
            go.Pie(
                values=[percent, 100 - percent],
                hole=0.75,
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=["#10b981", "#e5e7eb"],
                    line=dict(color="white", width=2)
                ),
            )
        ]
    )

    fig.update_layout(
        height=180,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{percent}%</b><br>{label}",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.set_page_config(page_title="Adaptive Learning Prototype", layout="centered")
def render_progress_donut(current_index, total_questions):
    completed = current_index
    remaining = max(total_questions - completed, 0)
    percent = int((completed / total_questions) * 100) if total_questions else 0

    fig = go.Figure(
        data=[
            go.Pie(
                values=[completed, remaining],
                hole=0.72,
                sort=False,
                direction="clockwise",
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=["#6366f1", "#e5e7eb"],
                    line=dict(color="white", width=4)
                ),
            )
        ]
    )

    fig.update_layout(
        height=220,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{percent}%</b><br>Complete",
                x=0.5,
                y=0.5,
                font=dict(size=22, color="#111827"),
                showarrow=False,
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---------------------------
# Helper functions
# ---------------------------
def initialize_session_state():
    if "question_order" not in st.session_state:
        st.session_state.question_order = list(range(len(questions)))
        random.shuffle(st.session_state.question_order)

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    if "selected_answer" not in st.session_state:
        st.session_state.selected_answer = None

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "questions_answered" not in st.session_state:
        st.session_state.questions_answered = 0

    if "mastery" not in st.session_state:
        st.session_state.mastery = {}

    if "topic_stats" not in st.session_state:
        st.session_state.topic_stats = {}
        
    if "topic_performance" not in st.session_state:
        st.session_state.topic_performance = {}


def get_current_question():
    current_question_number = st.session_state.question_order[st.session_state.current_index]
    return questions[current_question_number]


def update_mastery(question, is_correct):
    topic = question.get("topic", "General")
    subtopic = question.get("subtopic", "General")

    if topic not in st.session_state.topic_stats:
        st.session_state.topic_stats[topic] = {"correct": 0, "total": 0}

    st.session_state.topic_stats[topic]["total"] += 1
    if is_correct:
        st.session_state.topic_stats[topic]["correct"] += 1

    if subtopic not in st.session_state.mastery:
        st.session_state.mastery[subtopic] = 0.50

    if is_correct:
        st.session_state.mastery[subtopic] = min(1.0, st.session_state.mastery[subtopic] + 0.10)
    else:
        st.session_state.mastery[subtopic] = max(0.0, st.session_state.mastery[subtopic] - 0.10)


def go_to_next_question():
    if st.session_state.current_index < len(st.session_state.question_order) - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.current_index = 0
        random.shuffle(st.session_state.question_order)

    st.session_state.selected_answer = None
    st.session_state.submitted = False


# ---------------------------
# App setup
# ---------------------------
initialize_session_state()
question = get_current_question()
options = question.get("options", question.get("choices", {}))

st.title("Adaptive Learning Prototype")
st.subheader(f"Topic: {question.get('topic', 'General')}")

st.write(question["stem"])

# Build display list like "A: Full answer text"
option_labels = [f"{key}: {value}" for key, value in options.items()]

# Find the correct display label later if needed
correct_answer_key = question["correct_answer"]
correct_answer_text = options.get(correct_answer_key, "")
correct_display = f"{correct_answer_key}: {correct_answer_text}"

selected_label = st.radio(
    "Choose your answer:",
    option_labels,
    index=None,
    key=f"radio_q_{question['id']}"
)

# ---------------------------
# Submit logic
# ---------------------------
if not st.session_state.submitted:
    if st.button("Submit"):
        if selected_label is None:
            st.warning("Please select an answer before submitting.")
        else:
            st.session_state.selected_answer = selected_label.split(":", 1)[0].strip()
            st.session_state.submitted = True
            st.session_state.questions_answered += 1

            is_correct = st.session_state.selected_answer == correct_answer_key
            topic = question.get("topic", "Unknown")

        if topic not in st.session_state.topic_performance:
            st.session_state.topic_performance[topic] = {"correct": 0, "total": 0}

            st.session_state.topic_performance[topic]["total"] += 1

        if is_correct:
            st.session_state.topic_performance[topic]["correct"] += 1
        if is_correct:
            st.session_state.score += 1

        update_mastery(question, is_correct)
        st.rerun()

# ---------------------------
# Feedback section
# ---------------------------
if st.session_state.submitted:
    selected_key = st.session_state.selected_answer
    is_correct = selected_key == correct_answer_key

    st.markdown("---")

    if is_correct:
        st.success("Correct.")
    else:
        st.error("Incorrect.")

    st.write(f"**Correct answer:** {correct_display}")

    selected_text = options.get(selected_key, "")
    if selected_key and selected_text:
        st.write(f"**Your answer:** {selected_key}: {selected_text}")

    if "keyword_clue" in question:
        st.write(f"**Keyword clue:** {question['keyword_clue']}")

    if "rationale" in question:
        st.write("**Rationale:**")
        st.write(question["rationale"])

    incorrect_rationales = question.get("incorrect_rationales", {})
    if not is_correct and selected_key in incorrect_rationales:
        st.write("**Why your answer was not the best choice:**")
        st.write(incorrect_rationales[selected_key])

    if "learning_point" in question:
        st.write("**Learning point:**")
        st.write(question["learning_point"])

    if st.button("Next Question"):
        go_to_next_question()
        st.rerun()

# ---------------------------
# Progress section
# ---------------------------
st.markdown("---")
st.header("Progress")


total_answered = st.session_state.questions_answered
score = st.session_state.score

render_progress_donut(total_answered, len(questions))
def render_mastery_donut(label, value):
    percent = int(value * 100)

    fig = go.Figure(
        data=[
            go.Pie(
                values=[percent, 100 - percent],
                hole=0.75,
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=["#3b82f6", "#e5e7eb"],
                    line=dict(color="white", width=2)
                ),
            )
        ]
    )

    fig.update_layout(
        height=180,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{percent}%</b><br>{label}",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

if total_answered > 0:
    percent = score / total_answered
    st.write(f"**Score:** {score}/{total_answered} ({percent:.0%})")
else:
    st.write("**Score:** 0/0")

# ---------------------------
# Mastery section
# ---------------------------
st.header("Current Mastery")

if st.session_state.mastery:
    for subtopic, mastery_value in st.session_state.mastery.items():
       render_mastery_donut(subtopic, mastery_value)
    
else:
    st.write("No mastery data yet. Answer a question to begin tracking.")

# ---------------------------
# Topic performance
# ---------------------------
st.header("Topic Performance")

if st.session_state.topic_performance:
    for topic, stats in st.session_state.topic_performance.items():
        correct = stats["correct"]
        total = stats["total"]
        render_performance_donut(topic, correct, total)
else:
    st.write("No performance data yet.")
