import streamlit as st
import pandas as pd
from datetime import datetime, date, time

from database import (
    init_db,
    add_task,
    get_tasks,
    toggle_task,
    delete_task,
    update_task
)


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

init_db()

st.set_page_config(
    page_title="DailyRoutine AI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f8fc;
}

.task-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
    background: white;
    margin-bottom: 10px;
}

.big-title {
    font-size: 35px;
    font-weight: 700;
}

.subtitle {
    color: #666;
    font-size: 16px;
}

.progress-box {
    padding: 20px;
    border-radius: 15px;
    background: #ffffff;
    border: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

now = datetime.now()

st.markdown(
    '<div class="big-title">🤖 DailyRoutine AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal daily planner and routine assistant</div>',
    unsafe_allow_html=True
)

st.write("")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    selected_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    st.divider()

    st.subheader("📌 Quick Categories")

    category_filter = st.selectbox(
        "Category",
        [
            "All",
            "Study",
            "Work",
            "Fitness",
            "Personal",
            "Health",
            "Other"
        ]
    )

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Completed"
        ]
    )


# --------------------------------------------------
# GET TASKS
# --------------------------------------------------

tasks = get_tasks()

columns = [
    "id",
    "title",
    "description",
    "task_date",
    "task_time",
    "priority",
    "category",
    "repeat_days",
    "completed"
]

df = pd.DataFrame(tasks, columns=columns)


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

today_string = selected_date.strftime("%Y-%m-%d")

if not df.empty:

    selected_tasks = df[
        df["task_date"] == today_string
    ]

    total_tasks = len(selected_tasks)

    completed_tasks = len(
        selected_tasks[
            selected_tasks["completed"] == 1
        ]
    )

else:

    total_tasks = 0
    completed_tasks = 0


pending_tasks = total_tasks - completed_tasks

progress = (
    completed_tasks / total_tasks
    if total_tasks > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Total Tasks",
        total_tasks
    )

with col2:
    st.metric(
        "✅ Completed",
        completed_tasks
    )

with col3:
    st.metric(
        "⏳ Pending",
        pending_tasks
    )

with col4:
    st.metric(
        "📈 Progress",
        f"{int(progress * 100)}%"
    )


st.progress(progress)


# --------------------------------------------------
# AI ROUTINE ASSISTANT
# --------------------------------------------------

st.subheader("🤖 Routine Assistant")

if total_tasks == 0:

    assistant_message = (
        "You don't have any tasks scheduled for this day. "
        "Add some tasks below to start building your routine."
    )

elif progress == 1:

    assistant_message = (
        "🎉 Excellent! You completed everything scheduled "
        "for this day."
    )

elif progress >= 0.7:

    assistant_message = (
        "🔥 You're doing great! Most of your tasks are complete. "
        "Finish the remaining tasks to complete your routine."
    )

elif progress >= 0.4:

    assistant_message = (
        "👍 Good progress. You have completed several tasks. "
        "Focus on the next important task."
    )

else:

    assistant_message = (
        "💪 Start with your highest-priority task. "
        "Small progress is better than waiting for the perfect time."
    )


st.info(assistant_message)


# --------------------------------------------------
# ADD TASK
# --------------------------------------------------

st.subheader("➕ Add New Task")

with st.form("add_task_form"):

    col1, col2 = st.columns(2)

    with col1:

        title = st.text_input(
            "Task Name",
            placeholder="Example: Study Python"
        )

        description = st.text_area(
            "Description",
            placeholder="What do you need to do?"
        )

        task_date = st.date_input(
            "Date",
            value=selected_date
        )

    with col2:

        task_time = st.time_input(
            "Time",
            value=time(9, 0)
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Urgent"
            ]
        )

        category = st.selectbox(
            "Category",
            [
                "Study",
                "Work",
                "Fitness",
                "Personal",
                "Health",
                "Other"
            ]
        )

    repeat_days = st.multiselect(
        "Repeat on",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    submitted = st.form_submit_button(
        "➕ Add Task",
        use_container_width=True
    )

    if submitted:

        if not title.strip():

            st.error("Please enter a task name.")

        else:

            add_task(
                title.strip(),
                description,
                task_date.strftime("%Y-%m-%d"),
                task_time.strftime("%H:%M"),
                priority,
                category,
                ", ".join(repeat_days)
            )

            st.success("Task added successfully!")

            st.rerun()


# --------------------------------------------------
# TASK LIST
# --------------------------------------------------

st.subheader(
    f"📅 Tasks for {selected_date.strftime('%A, %d %B %Y')}"
)


if df.empty:

    st.info(
        "No tasks yet. Add your first task above."
    )

else:

    filtered = df[
        df["task_date"] == today_string
    ].copy()

    if category_filter != "All":

        filtered = filtered[
            filtered["category"] == category_filter
        ]

    if status_filter == "Pending":

        filtered = filtered[
            filtered["completed"] == 0
        ]

    elif status_filter == "Completed":

        filtered = filtered[
            filtered["completed"] == 1
        ]


    if filtered.empty:

        st.info("No matching tasks.")

    else:

        for _, task in filtered.iterrows():

            task_id = int(task["id"])

            completed = bool(
                task["completed"]
            )

            col1, col2, col3, col4 = st.columns(
                [0.07, 0.48, 0.20, 0.15]
            )

            with col1:

                checked = st.checkbox(
                    "Done",
                    value=completed,
                    key=f"check_{task_id}",
                    label_visibility="collapsed"
                )

                if checked != completed:

                    toggle_task(
                        task_id,
                        int(checked)
                    )

                    st.rerun()

            with col2:

                if completed:

                    st.markdown(
                        f"### ~~{task['title']}~~"
                    )

                else:

                    st.markdown(
                        f"### {task['title']}"
                    )

                st.caption(
                    f"{task['description']} | "
                    f"📂 {task['category']} | "
                    f"⚡ {task['priority']}"
                )

            with col3:

                st.markdown(
                    f"🕐 **{task['task_time']}**"
                )

                if task["repeat_days"]:

                    st.caption(
                        f"🔁 {task['repeat_days']}"
                    )

            with col4:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task_id}"
                ):

                    delete_task(task_id)

                    st.rerun()

            st.divider()


# --------------------------------------------------
# AI DAILY PLAN
# --------------------------------------------------

st.subheader("🧠 AI Daily Plan")

if not df.empty:

    today_tasks = df[
        df["task_date"] == today_string
    ].sort_values(
        "task_time"
    )

    if len(today_tasks) > 0:

        st.write(
            "Here is your suggested order for the day:"
        )

        for i, (_, task) in enumerate(
            today_tasks.iterrows(),
            start=1
        ):

            status = (
                "✅"
                if task["completed"]
                else "⬜"
            )

            st.write(
                f"{i}. {status} "
                f"**{task['task_time']}** — "
                f"{task['title']} "
                f"({task['priority']})"
            )

    else:

        st.info(
            "Add tasks to generate your daily plan."
        )

else:

    st.info(
        "Add tasks to generate your daily plan."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    f"Current time: {now.strftime('%I:%M:%S %p')} | "
    f"DailyRoutine AI"
)