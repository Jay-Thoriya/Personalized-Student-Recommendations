import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
from collections import Counter
from datetime import datetime
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)


# Load Data for Analysis & Insights
with open("data/quiz_data.json", "r") as file:
    data = json.load(file)
df = pd.json_normalize(data, sep='.')

df['accuracy'] = df['accuracy'].str.replace('%', '').astype(float)
df['final_score'] = df['final_score'].astype(float)
df['negative_score'] = df['negative_score'].astype(float)

difficulty_mapping = {1: "Easy", 2: "Medium", 3: "Hard"}
df['difficulty_level'] = df['trophy_level'].map(difficulty_mapping)

df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["date"] = df["submitted_at"].dt.date  

# Load Quiz Data
with open("data/quiz_all_data.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

quiz = quiz_data.get("quiz", {})
questions = quiz.get("questions", [])


# Convert number into level of exam


# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Select Section", ["Analysis & Graphs", "Insights & Trends","Recommendations","Quiz Submission Summary" ,"Quiz Questions Viewer" , "Personal Ai Assistant"])

# Section 1: Analysis & Graphs
if section == "Analysis & Graphs":
    st.title("📊 Student Performance Analysis")
    graph_option = st.selectbox("Select Graph", ["Overview", "Score Analysis", "Performance Trends", "Difficulty Insights", "Topic", 'quiz overview'])
    



    if graph_option == "quiz overview":
        # Calculate required metrics
        df['attempted_questions'] = df['correct_answers'] + df['incorrect_answers']
        
        # Calculate averages
        average_total = df['total_questions'].mean()
        average_attempted = df['attempted_questions'].mean()
        average_correct = df['correct_answers'].mean()
        average_incorrect = df['incorrect_answers'].mean()

        # Pie Chart Data
        metrics = ['Total Questions', 'Attempted Questions', 'Correct Answers', 'Incorrect Answers']
        averages = [average_total, average_attempted, average_correct, average_incorrect]

        # Plotting the Pie Chart
        fig, ax = plt.subplots()
        ax.pie(averages, labels=metrics, autopct='%1.1f%%', colors=['skyblue', 'orange', 'lightgreen', 'tomato'])
        ax.set_title("Average Question Statistics")

        # Display the chart
        st.pyplot(fig)

    # Main Dashboard

    df["submitted_at"] = pd.to_datetime(df["submitted_at"]) 
    df["date"] = df["submitted_at"].dt.date  

    if graph_option == "Overview":
        st.subheader("📌 Data Overview")
        # Ensure 'attempt' column exists
        if 'attempt' not in df.columns:
            df['attempt'] = range(1, len(df) + 1)
        
        st.dataframe(df[['date', 'quiz.title','quiz.topic', 'difficulty_level','total_questions','correct_answers','incorrect_answers','score','final_score', 'speed','accuracy', 'better_than','rank_text','mistakes_corrected','initial_mistake_count']])


    elif graph_option == "Score Analysis":
        st.subheader("📈 Score Progression")
        df['attempt'] = range(1, len(df) + 1)
        fig = px.line(df, x='attempt', y='final_score', markers=True, title="Score Progression Over Attempts", line_shape='spline')
        st.plotly_chart(fig, use_container_width=True)

        # Title
        st.subheader("📊 Performance Insights :")

        st.write("- **Potential knowledge gaps** or challenges during those attempts.")
        st.write("- **Lack of steady improvement trend.**")
        st.write("- **Inconsistent learning** or preparation patterns suggested.")

        # Recommendations for Improvement
        st.subheader(" Recommendations for Improvement ")

        st.subheader("⚠️ Address Inconsistent Performance :")
        st.write("- **Identify Root Causes:** Investigate factors contributing to score fluctuations.")
        st.write("- **Enhance Consistency:** Establish a regular study schedule and focus on conceptual clarity.")

        # Plot the distribution of final scores
        st.write("### Final Score Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['final_score'], bins=10, kde=True, ax=ax)
        ax.set_title('Final Score Distribution')
        ax.set_xlabel('Final Score')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)


    elif graph_option == "Performance Trends":
        import plotly.express as px

        # Ensure 'attempt' column exists
        if 'attempt' not in df.columns:
            df['attempt'] = range(1, len(df) + 1)


        st.subheader("📊 Accuracy & Mistakes Analysis")
        
        # Accuracy Trend
        fig = px.bar(df, x='attempt', y='accuracy', title="Accuracy Trend", color='accuracy', color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Recommendations for Improvement:**")
        st.write("*Accuracy Improvement :*")
        st.write('- Minimize penalties by avoiding blind guesses.')
        st.write("- Work on strategies for eliminating incorrect answer choices.")
        
        # Scatter Plot: Mistakes corrected vs. Initial mistakes
        fig = px.scatter(df, x='initial_mistake_count', y='mistakes_corrected',
                        size='final_score', color='accuracy', title="Mistakes Corrected vs. Initial Mistakes")
        st.plotly_chart(fig, use_container_width=True)

    elif graph_option == "Difficulty Insights":
        st.subheader("🎯 Performance Based on Difficulty Level")
        
        # Box Plot: Performance vs. Difficulty Level
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x='difficulty_level', y='final_score', data=df, ax=ax, palette="coolwarm")
        ax.set_title("Performance Based on Difficulty Level",fontsize=5)
        st.pyplot(fig)
        
        st.write("**Performance Insights:**")
        st.write("*Difficulty Level Analysis:*")
        st.write("- Easy: Average score of 66, with consistent but moderate variability.")
        st.write("- Medium: Average score of 68.7, with wide fluctuations (ranging from 5 to 115)")
        st.write("- Hard: Average score of 29.8, indicating significant challenges at higher difficulty levels.")
        
        st.write("**Recommendations for Improvement:**")
        st.write("*Focus on Hard Questions:*")
        st.write("The student should practice more on hard-level questions to build familiarity and confidence. Suggested practice sets:")
        st.write("- Time-bound quizzes to simulate exam conditions.")
        st.write("- Conceptual questions from weak topics.")
        

        # Trophy Level Distribution
        fig, ax = plt.subplots()
        sns.countplot(x='difficulty_level', data=df, ax=ax, palette='magma')
        ax.set_title("Distribution of Difficulty Levels")
        st.pyplot(fig)

        st.write("**Recommendations for Improvement:**")
        st.write("*Medium-Level Consistency:*")
        st.write("- Given the variability in scores for medium-level quizzes, the student should maintain a structured revision strategy to stabilize performance.")
        

    elif graph_option == "Topic":
        st.subheader("🎯 Performance Based on Topic ")
        
        # Box Plot: Performance vs. Difficulty Level
        # Pie chart: Topic Distribution
        topic_counts = df['quiz.topic'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(topic_counts, labels=topic_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        st.pyplot(fig)

        st.write("**Performance Insights:**")
        st.write("*Topic Analysis:*")
        st.write("- Strong performance in 'Human health and disease'  (average score: 110) and 'Body Fluids and Circulation' (average score: 78.6).")
        st.write("- Weak areas include 'principles of inheritance and variation' (average score: 5) and 'Respiration and Gas Exchange' (average score: 21).")

        st.write("**Recommendations for Improvement:**")
        st.write("*Target Weak Topics:*")
        st.write('- Focus on "principles of inheritance and variation" and "Respiration and Gas Exchange."')
        st.write("- Allocate time for understanding foundational concepts through video lectures or tutoring sessions.")

# Section 2: Insights & Trends
elif section == "Insights & Trends":
    st.title("📊 Insights & Trends")
    insight_option = st.selectbox("Select Insight", ["Weak Areas", "Improvement Trend", "Performance Gaps"])
    with open("data\quiz_data.json", "r") as file:
        data = json.load(file)

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Extract relevant fields
    df["topic"] = df["quiz"].apply(lambda x: x["topic"])
    df["accuracy"] = df["accuracy"].str.replace("%", "").astype(float)
    df["incorrect_answers"] = df["incorrect_answers"].astype(int)
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])

    def plot_weak_areas():
        weak_areas = df.groupby("topic")["incorrect_answers"].sum().sort_values(ascending=False)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=weak_areas.index, y=weak_areas.values, palette="Reds_r")
        plt.xticks(rotation=45, ha='right')
        plt.title("Weak Areas by Incorrect Answers")
        plt.xlabel("Topic")
        plt.ylabel("Total Incorrect Answers")
        st.pyplot(plt)


        st.subheader("📌 Recommendations for Improvement")

        # Prioritize "Body Fluids and Circulation"
        st.subheader("🎯 Prioritize \"Body Fluids and Circulation\"")
        st.write("- **Targeted Review:** Focus on key concepts and processes.")
        st.write("- **Practice Questions:** Solve numerous practice questions.")
        st.write("- **Seek Help:** Consult teachers or tutors for clarification.")

        # Address "Reproductive Health" and "Human Reproduction"
        st.subheader("📌 Address \"Reproductive Health\" and \"Human Reproduction\"")
        st.write("- **Similar Strategies:** Apply the same targeted review and practice methods.")
        st.write("- **Identify Weaknesses:** Pinpoint specific sub-topics causing issues.")

        # Improve "Respiration and Gas Exchange"
        st.subheader("📌 Improve \"Respiration and Gas Exchange\"")
        st.write("- **Targeted Practice:** Focus on questions related to this topic.")
        st.write("- **Analyze Errors:** Understand the reasons behind mistakes.")

        # Maintain Strong Areas
        st.subheader("✅ Maintain Strong Areas")
        st.write("- **Regularly revise:** \"Reproductive Health,\" \"Human Health and Disease,\" and \"Microbes in Human Welfare.\"")
        st.write("- **Regular Revision:** Reinforce knowledge retention.")
        st.write("- **Mixed Quizzes:** Include these topics in mixed quizzes.")

        # General Recommendations
        st.subheader("📊 General Recommendations")
        st.write("- **Error Analysis:** Analyze all incorrect answers to identify recurring patterns.")
        st.write("- **Active Learning:** Utilize techniques like teaching concepts and creating summaries.")
        st.write("- **Mock Tests:** Simulate exam conditions with regular mock tests.")

        st.success("Consistent effort and a strategic approach will lead to significant improvement!")


    def plot_improvement_trend(df):
        
    


        df = pd.DataFrame(data)
        # Convert submitted_at to datetime and extract only the date (YYYY-MM-DD)
        df["submitted_at"] = pd.to_datetime(df["submitted_at"]) 
        df["date"] = df["submitted_at"].dt.date  

        # ✅ Clean and convert accuracy values
        df["accuracy"] = df["accuracy"].astype(str).str.replace('%', '', regex=True)  # Remove '%'
        df["accuracy"] = pd.to_numeric(df["accuracy"], errors='coerce')  # Convert to float
        df = df.dropna(subset=["accuracy"])  # Drop rows where conversion failed



        # ✅ Plot the Improvement Trend Over Time
        st.subheader('Performance Trend Accuracy')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=df["date"], y=df["accuracy"], color="red", marker="o", label="Daily Average", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title("Improvement Trend Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Accuracy")
        ax.legend()
        st.pyplot(fig)



        scores = [108, 92, 116, 36, 36,40, 36,12, 76, 40,112, 64, 52, 24]  # Replace with actual historical data
        final_score = [105,92,115,35,16,24,27,5,76,40,110,61,35,21]
        # Convert submitted_at to datetime and extract only the date (YYYY-MM-DD)
        df["submitted_at"] = pd.to_datetime(df["submitted_at"]) 
        df["date"] = df["submitted_at"].dt.date

        st.subheader('Performance Trend score')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=df["date"], y=scores, marker="o", linestyle="-", color="b", label="Score Trend", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title("Improvement Trend Over Time")
        ax.set_xlabel("Data")
        ax.set_ylabel("Average score")
        ax.legend()
        st.pyplot(fig)

        st.subheader('Performance Trend Final Score')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=df["date"], y=final_score, marker="o", linestyle="-", color="g", label="Score Trend", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title("Improvement Trend Over Time")
        ax.set_xlabel("Data")
        ax.set_ylabel("Average Final Score")
        ax.legend()
        st.pyplot(fig)

        st.subheader('Performance Trend Speed')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=df["date"], y=df["speed"], color="orange", marker="o", label="Daily Average", ax=ax)
        plt.xticks(rotation=45, ha='right')
        ax.set_title("Improvement Trend Over Speed")
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Speed")
        ax.legend()
        st.pyplot(fig)



    def plot_performance_gaps():
        performance = df.groupby("topic")["accuracy"].mean().sort_values()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=performance.index, y=performance.values, palette="coolwarm")
        plt.xticks(rotation=45, ha='right')
        plt.title("Performance Gaps Across Topics")
        plt.xlabel("Topic")
        plt.ylabel("Average Accuracy (%)")
        st.pyplot(plt)

        st.subheader("📌 Recommendations for Improvement")

        # Prioritize Weak Areas
        st.subheader("🎯 Prioritize Weak Areas")
        st.write("- **Focus on:** \"Principles of Inheritance and Variation,\" \"Human Reproduction,\" and \"Reproductive Health.\"")
        st.write("- **Targeted Review:** Revisit core concepts and related materials.")
        st.write("- **Conceptual Questions:** Practice conceptual questions to solidify understanding.")
        st.write("- **Topical Quizzes:** Assess knowledge gaps with topic-specific quizzes.")
        st.write("- **Seek Assistance:** Consult teachers, tutors, or classmates for support.")

        # Address Moderate Performance
        st.subheader("📌 Address Moderate Performance")
        st.write("- **Focus Areas:** \"Respiration and Gas Exchange\" and \"Body Fluids and Circulation\" require additional attention.")
        st.write("- **Targeted Practice:** Focus on questions related to these topics.")
        st.write("- **Error Analysis:** Analyze mistakes to identify areas for improvement.")

        # Maintain Strong Areas
        st.subheader("✅ Maintain Strong Areas")
        st.write("- **Regular Revision:** Reinforce learning through consistent review.")
        st.write("- **Mixed Quizzes:** Include these topics in mixed quizzes to ensure broad retention.")

        # General Recommendations
        st.subheader("📊 General Recommendations")
        st.write("- **Error Analysis:** Analyze incorrect answers across all topics to identify recurring mistakes.")
        st.write("- **Active Learning:** Employ active learning techniques like teaching concepts to others and creating summaries.")
        st.write("- **Mock Tests:** Simulate exam conditions with regular mock tests.")

        st.success("Consistent effort and a strategic approach will lead to significant improvement!")

    st.write(" ")
    st.write(" ")
    st.write(" ")   
    st.write(" ")
    st.write(" ")

    if insight_option == "Weak Areas":
        plot_weak_areas()
    if insight_option == "Improvement Trend":
        plot_improvement_trend(df)
    if insight_option == "Performance Gaps":
        plot_performance_gaps()
    
# Section 3: Quiz Questions Viewer
elif section == "Recommendations":
    
    
    # Title
    st.title("📌 Personalized Insights & Recommendations")

    # Weak Areas
    st.header("🔴 Weak Areas (Overall Performance)")
    st.write("**Accuracy:** The overall accuracy of **65.64%** indicates a significant area for improvement. While speed is good, correct answers are more crucial for NEET.")
    st.write("**Performance on Hard Difficulty Questions:** The substantial drop in scores, speed, and accuracy on hard questions is a major red flag. This suggests a lack of conceptual understanding or application skills needed for more challenging problems.")

    # Strong Areas
    st.header("🟢 Strong Areas (Overall Performance)")
    st.write("**Speed:** The average speed of **85.5%** is commendable. The student can likely complete exams within the allotted time. This is a valuable asset.")
    st.write("**Performance on Easy Questions:** Mastery of easy questions is excellent. This builds a good foundation and ensures easy marks are secured.")
    st.write("**Performance on Medium Questions:** The student performs reasonably well on medium-difficulty questions, suggesting a good grasp of core concepts.")

    # Topics Showing Improvement
    st.header("📈 Topics Showing Improvement")
    st.write("**Difficult to determine with limited data:** With only **14 records** and no chronological tracking of performance on the same topic over multiple attempts, it's impossible to identify improvement trends. More data points over time are needed.")

    # Topics Needing Immediate Attention
    st.header("⚠️ Topics Needing Immediate Attention")
    st.write("- **Body Fluids and Circulation (Hard):** This topic appears multiple times with 'Hard' difficulty, and the performance is consistently low. This is a high-priority area.")
    st.write("- **Human Reproduction (Hard):** This topic also shows weaker performance in the hard difficulty level.")

    # Exam Strategy Insights
    st.header("📊 Exam Strategy Insights")
    st.write("- **Focus on Accuracy over Speed (in Hard Questions):** While speed is good, the student needs to prioritize accuracy, especially on hard questions. Slowing down slightly to ensure better understanding and reduce careless mistakes could be beneficial.")
    st.write("- **Time Management (Overall):** The good speed suggests effective time management. However, the student should ensure they allocate sufficient time to review answers, especially in hard sections.")

    # Actionable Recommendations for Improvement
    st.header("🎯 Actionable Recommendations for Improvement")
    st.write("- **Targeted Practice (Hard Questions):** Focus specifically on practicing hard-level questions, especially in *Body Fluids and Circulation* and *Human Reproduction.* Seek out challenging practice problems, mock tests, and previous years' NEET papers.")
    st.write("- **Conceptual Clarity:** Review the underlying concepts for the weak topics. Use textbooks, online resources, or seek help from teachers/mentors to strengthen understanding. A strong conceptual foundation is crucial for tackling hard questions.")
    st.write("- **Accuracy Drills:** Practice solving questions with a focus on accuracy rather than speed. Start by solving a few questions slowly and deliberately, focusing on understanding each step. As accuracy improves, gradually increase speed.")
    st.write("- **Mock Tests and Analysis:** Take regular mock tests that include a good mix of difficulty levels. After each test, thoroughly analyze performance, paying close attention to incorrect answers and identifying the reasons for mistakes (lack of understanding, careless errors, etc.).")
    st.write("- **Topic-wise Revision:** Regularly revise all topics, but dedicate extra time to the weaker areas. Use flashcards, mind maps, or other effective revision techniques.")
    st.write("- **Seek Expert Guidance:** If possible, consult with teachers, mentors, or experienced NEET tutors. They can provide personalized feedback, identify blind spots, and suggest effective study strategies.")
    st.write("- **Consistent Effort:** Consistent and dedicated effort is key to success in NEET. Maintain a regular study schedule and stick to it as much as possible.")


    recommendations = [
        "✔️ Prioritize weak topics and practice more questions in those areas.",
        "✔️ Work on **accuracy** before speed; slow down and read questions carefully.",
        "✔️ Reduce incorrect answers by avoiding random guessing.",
        "✔️ Focus on conceptual clarity before attempting hard-level quizzes.",
        "✔️ Practice exam-style questions to improve speed and confidence.",
        "✔️ Take topic-wise timed tests to simulate real exam conditions.",
        "✔️ Use previous mistakes as learning points and revise difficult questions."
    ]
    
    for rec in recommendations:
        st.markdown(rec)

# Section 4: Quiz Questions Viewer
elif section == "Quiz Submission Summary":
    def get_exam_level(trophy_level):
        level_map = {
        1: "Easy",
        2: "Medium",
        3: "Hard"
    }
        return level_map.get(trophy_level, "Invalid Trophy Level")

    # Group quizzes by date
    quizzes_by_date = {}
    for quiz in data:
        start_time = datetime.strptime(quiz['started_at'], "%Y-%m-%dT%H:%M:%S.%f+05:30")
        quiz_date = start_time.strftime('%x')  # Format as MM/DD/YY
        
        if quiz_date not in quizzes_by_date:
            quizzes_by_date[quiz_date] = []
        quizzes_by_date[quiz_date].append(quiz)
    st.sidebar.title("Select Date")
    selected_date = st.sidebar.selectbox("Choose a date:", list(quizzes_by_date.keys()))

    st.title(f"Quiz Summary for {selected_date}")
    quizzes_on_selected_date = quizzes_by_date[selected_date]
    st.write(f"Total quizzes taken on {selected_date}: {len(quizzes_on_selected_date)}")

    # Select a quiz
    selected_quiz_id = st.selectbox(
        "Select a quiz to view details:",
        [f"Quiz {i+1}: {quiz['quiz']['title']}" for i, quiz in enumerate(quizzes_on_selected_date)]
    )

    # Find the selected quiz details
    selected_quiz = quizzes_on_selected_date[
        [f"Quiz {i+1}: {quiz['quiz']['title']}" for i, quiz in enumerate(quizzes_on_selected_date)].index(selected_quiz_id)
    ]

    # Display quiz details
    if selected_quiz:
        st.subheader("Quiz Details")
        st.write(f"**Question Topic:** {selected_quiz['quiz']['topic']}")
        st.write(f"**Difficulty Level:** {get_exam_level(selected_quiz['trophy_level'])}")
        st.write(f"**Total Questions:** {selected_quiz['total_questions']}")
        
        start_time = datetime.strptime(selected_quiz['started_at'], "%Y-%m-%dT%H:%M:%S.%f+05:30")
        end_time = datetime.strptime(selected_quiz['ended_at'], "%Y-%m-%dT%H:%M:%S.%f+05:30")
        time_taken = round((end_time - start_time).total_seconds() / 60, 2)  # Convert to minutes
        st.write(f"**Time Taken:** {time_taken} minutes")
        st.write(f"**Total Questions**: {selected_quiz['total_questions']}")

        
        st.subheader("Quiz Response Analysis")
        
        
        # Bar chart for correct vs incorrect answers
        #fig, ax = plt.subplots()
        # ax.bar(['Correct', 'Incorrect'], [selected_quiz['correct_answers'], selected_quiz['incorrect_answers']], color=['green', 'red'])
        # ax.set_ylabel("Number of Questions")
        # ax.set_title("Correct vs Incorrect Answers")
        # st.pyplot(fig)



        # # Calculate averages
        # attempted = selected_quiz['correct_answers'] + selected_quiz['incorrect_answers']
        # Refuse = selected_quiz['total_questions'] - attempted
        # correct = selected_quiz['correct_answers']
        # incorrect = selected_quiz['incorrect_answers']
        # st.write(f"**attempted**: {attempted} , Refuse : {Refuse}  ✅ : {correct} , ❌ : {incorrect}")
        # # Pie Chart Data
        # metrics = ['Not Attempted Questions', 'Attempted Questions', 'Correct Answers', 'Incorrect Answers']
        # averages = [Refuse, attempted, correct, incorrect]
        # print(averages)
        # # Plotting the Pie Chart
        # fig, ax = plt.subplots()
        # ax.pie(averages, labels=metrics, autopct='%1.f', colors=['skyblue', 'orange', 'lightgreen', 'tomato'])
        # ax.set_title("Average Question Statistics")
        # st.pyplot(fig)

        # Example values
        # Given values (replace with selected_quiz values)
        total_questions = selected_quiz['total_questions']
        correct = selected_quiz['correct_answers']
        incorrect = selected_quiz['incorrect_answers']
        not_attempted = total_questions - (correct + incorrect)

        total_questions = selected_quiz['total_questions']  # Example of a non-100 total
        correct = selected_quiz['correct_answers']
        incorrect = selected_quiz['incorrect_answers']
        attempted = correct + incorrect
        Refuse = total_questions - attempted

        metrics = ['Not Attempted Questions', 'Correct Answers', 'Incorrect Answers']
        values = [not_attempted, correct, incorrect]

        # Define colors
        colors = ['skyblue', 'lightgreen', 'tomato']

        # Define explode values (optional: highlight incorrect answers)
        explode = (0.1, 0.0, 0.2)  

        # Define wedge properties
        wp = {'linewidth': 1, 'edgecolor': "black"}

        # Define formatting function for percentages & absolute values
        def func(pct, allvalues):
            absolute = int(pct / 100. * np.sum(allvalues))
            return "{:.1f}%\n({:d} Qs)".format(pct, absolute)  # 'Qs' for questions

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(values,
                                        autopct=lambda pct: func(pct, values),  
                                        explode=explode,
                                        labels=metrics,
                                        shadow=True,
                                        colors=colors,
                                
                                        wedgeprops=wp,
                                        textprops=dict(color="black"))  

        # Add a legend
        ax.legend(wedges, metrics,
                title="Quiz Metrics",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        # Adjust text properties
        plt.setp(autotexts, size=10, weight="bold")

        # Set title
        ax.set_title("Student Performance Breakdown")

        # Show in Streamlit
        st.pyplot(fig)


        st.subheader("Overall Performance Metrics")
        st.write(f"**Accuracy:** {selected_quiz['accuracy']}")
        st.write(f"**Speed:** {selected_quiz['speed']}")
        st.write(f"**Score:** {selected_quiz['score']}")
        st.write(f"**Final Score:** {selected_quiz['final_score']}")
        st.write(f"**Mistakes Corrected:** {selected_quiz['mistakes_corrected']}")
        st.write(f"**Initial Mistake Count:** {selected_quiz['initial_mistake_count']}")
        st.write(f"**Rank:** {selected_quiz['rank_text']}")
        st.write(f"**Better Than:** {selected_quiz['better_than']}%")





# Section 5: Quiz Questions Viewer
elif section == "Quiz Questions Viewer":

    st.title("Quiz Viewer")
    st.subheader(f"Topic: {quiz.get('topic', 'Unknown')}")
    
    
    for i, question in enumerate(questions, start=1):
        st.write("---")
        st.write(f"### Question {i}:")
        st.write(f"**Question:** {question['description']}")
        options = question.get("options", [])
        for option in options:
            st.write(f"- {option['description']}")
        correct_answer = next((opt['description'] for opt in options if opt['is_correct']), "No correct answer found")
        st.write(f"✅ **Correct Answer:** {correct_answer}")


elif section == "Personal Ai Assistant":

    st.title("Personal Student Advisor Chatbot")

    # Load the student's report from a text file
    def load_student_report(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error loading student report: {e}"

    student_report = load_student_report("data\student_overall_report.txt")

    # Create a system prompt that incorporates the student's report
    # System prompt incorporating student data
    system_prompt = f"""
    You are a personal AI tutor. Your job is to guide students based on their performance report.
    Below is the student's report:

    {student_report}

    Your responses should be:
    - Encouraging and motivating
    - Focused on improving weak areas
    - Providing actionable steps for better performance
    - Answering the student's questions accurately

    if you need more information, please ask the student for clarification.

    if student ask outside the scope of the report, please politely tell them you can't help with that.
    """

    # Initialize conversation history in session_state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "Hi there! I'm here to help you improve your scores. How can I assist you today?"}
        ]

    # Display previous chat messages (excluding system messages)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input through a chat input box
    user_input = st.chat_input("Ask me anything about your performance...")

    if user_input:
        # Append user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Check if the user greets the bot
        greetings = ["hi", "hello", "hey"]
        if user_input.lower().strip() in greetings:
            bot_reply = "Hello! How can I assist you with your studies today?"
        else:
            # Send chat history to AI model for response
            conversation = [msg["content"] for msg in st.session_state.messages]

            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(conversation)
                bot_reply = response.text if response and hasattr(response, "text") else "Sorry, I couldn't process that."
            except Exception as e:
                bot_reply = f"⚠️ Error generating response: {e}"

        # Append and display assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)


