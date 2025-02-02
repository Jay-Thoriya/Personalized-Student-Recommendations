# Personalized Student Recommendations

This project provides personalized recommendations to students based on their quiz performance, helping them improve their preparation for competitive exams like NEET. The solution leverages two datasets to analyze quiz performance and generate actionable insights for the users. Additionally, a chatbot is included to facilitate conversations related to their studies.

## Steps to Run the Project

1. **Clone the repository**  
   First, clone the repository to your local machine by running the following command:

      ```bash
      git clone https://github.com/Jay-Thoriya/Personalized-Student-Recommendations.git


2. **Install required dependencies**
  Navigate into the project directory and install the necessary dependencies using pip:

       ```bash
         cd Personalized-Student-Recommendations
   
         pip install -r requirements.txt

3. **Set up the .env file**
   To run the chatbot, create a .env file in the root directory of the project and add your GOOGLE_API_KEY:
   
      ```bash
      GOOGLE_API_KEY=your_google_api_key_here


You will need to obtain a valid Google API key to access the chatbot functionality.



5. **Run the dashboard**
    After installing the dependencies, you can launch the dashboard with Streamlit:


       streamlit run dashboard.py


6. **Access the dashboard**
    Once the application is running, it will be accessible via your browser at the provided local address.



**Project Structure**
- dashboard.py: The main application file that runs the Streamlit dashboard.
- requirements.txt: A list of Python dependencies required for the project.
- data/: Directory containing the datasets used for analysis.


**Visualizations and Insights**
- Screenshots of key visualizations and insights are included in this repository.
- The insights help users identify their weak areas and receive recommendations for improvement.

**Chatbot Integration**:
- A chatbot is included to provide personalized conversations with students, assisting them with study-related questions and offering guidance based on their performance data.
