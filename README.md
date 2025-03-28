🌍 Population Analysis Dashboard with AI Chatbot
🚀 An interactive Streamlit dashboard that visualizes population data and allows AI-driven queries for insights.

📌 Features
📂 Upload CSV to process and analyze population data.

📊 Multiple visualization options: Bar Chart, Line Chart, Pie Chart, and Choropleth Map.

🔍 AI-powered chatbot using OpenAI & LangChain to filter data based on user queries.

📅 Year-wise population trend analysis.

🔠 Alphabetical filter (A-Z buttons) for country selection.

📉 Mean population calculation with dynamic filtering.

🛠️ Tech Stack
Frontend: Streamlit

Backend: FastAPI

AI & NLP: OpenAI API, LangChain

Data Handling: Pandas, NumPy

Visualization: Plotly

🚀 Installation & Setup
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/Vansh-Gupta/Population-Dashboard-AI.git
cd Population-Dashboard-AI

2️⃣ Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up OpenAI API Key

Create a .env file and add:

bash
Copy
Edit
OPENAI_API_KEY=your_openai_api_key

5️⃣ Run the FastAPI Backend
bash
Copy
Edit
uvicorn backend:app --reload

6️⃣ Run the Streamlit Frontend
bash
Copy
Edit
streamlit run app.py
🎯 Usage
Upload a CSV file containing population data.

Enter queries like:

"Show me data for China and India from 2001 to 2015."

"Compare population trends in the USA and Brazil."

Filter data using year range and alphabetical buttons.

Select chart type for better visualization.



📌 Future Improvements
✅ Add real-time data fetching.

✅ Improve AI chatbot capabilities.

✅ Enable database storage for uploaded files.



