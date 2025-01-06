import streamlit as st
import pandas as pd
import json
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import openai

# Get API key
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set page configuration and title for Streamlit
st.set_page_config(page_title="ChatWithJSON", page_icon="📊", layout="wide")

# Add header with title and description
st.markdown(
    """
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
        <h1 style="color: #333; font-size: 40px; text-align: center;">📊 ChatWithJSON</h1>
        <p style="color: #555; font-size: 18px; text-align: center;">Interact with your JSON file and get insights using AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Function to interact with the JSON file
def chat_with_json(df, prompt):
    llm = OpenAI(api_token=OPENAI_API_KEY)
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt)
    return result

# Placeholder for the uploaded file
uploaded_file_path = 'E:/Downloads/csvGPT-main/Chat_with_csv/sataging_data'  # Path for the uploaded file

if uploaded_file_path:
    st.info("📂 JSON Uploaded Successfully")

    # Safely read the file and handle multi-line or concatenated JSON
    try:
        with open(uploaded_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Parse each line as JSON
        json_data = [json.loads(line) for line in lines if line.strip()]
    except (UnicodeDecodeError, json.JSONDecodeError):
        st.error("❌ Error reading JSON file. Ensure it is properly formatted.")
        json_data = []

    # Convert JSON to DataFrame for analysis
    if json_data:
        data = pd.json_normalize(json_data) if isinstance(json_data, list) else pd.json_normalize([json_data])
        st.write("### Data Preview")
        st.dataframe(data, use_container_width=True)
    else:
        st.warning("⚠️ No valid data found in the JSON file.")

    # Create a two-column layout for user query and output
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.info("💬 Chat Below")
        input_text = st.text_area("Enter your query")

    with right_col:
        st.write("### 📋 Output")
        st.markdown(
            """
            <div style="background-color: black; color: white; border: 1px solid #ccc; padding: 10px; 
                        border-radius: 5px; overflow-wrap: break-word; height: 300px; overflow-y: auto;">
                Your output will appear here once you submit your query.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if input_text:
        st.info(f"Your Query: **{input_text}**")

        # Generate summary if query contains "summary"
        if "summary" in input_text.lower():
            with left_col:
                st.info("🔄 Generating Summary...")
                try:
                    predefined_queries = [
                        "Provide key statistics for the data",
                        "Highlight trends or anomalies",
                        "Summarize important insights",
                        "List the most frequent values for each column",
                        "Identify outliers in the data",
                        "Provide correlations or patterns between columns",
                    ]
                    summary_results = []
                    for query in predefined_queries:
                        summary_results.append(chat_with_json(data, query))

                    with right_col:
                        st.write("### 📜 Summary Report")
                        for i, res in enumerate(summary_results):
                            with st.expander(f"Query {i+1}: {predefined_queries[i]}"):
                                st.markdown(
                                    f"""
                                    <div style="background-color: black; color: white; border: 1px solid #ccc; 
                                                padding: 10px; border-radius: 5px; overflow-wrap: break-word;">
                                        {res}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                except Exception as e:
                    st.error(f"❌ Error generating summary: {e}")
        else:
            # Process individual query
            try:
                result = chat_with_json(data, input_text)
                with right_col:
                    st.write("### 📋 Result")
                    st.markdown(
                        f"""
                        <div style="background-color: black; color: white; border: 1px solid #ccc; 
                                    padding: 10px; border-radius: 5px; overflow-wrap: break-word;">
                            {result}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"❌ Error processing query: {e}")

# Hide Streamlit header, footer, and menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

# Apply CSS code to hide header, footer, and menu
st.markdown(hide_st_style, unsafe_allow_html=True)
