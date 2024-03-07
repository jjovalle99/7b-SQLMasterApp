from dotenv import load_dotenv

load_dotenv()
import os

import pandas as pd
import streamlit as st
from langchain.prompts import PromptTemplate
from llama_index.llms.sagemaker_endpoint import SageMakerLLM
from pandasql import sqldf

generation_args = {
    "max_new_tokens": 100,
    "do_sample": True,
    "temperature": 0.3,
    "top_k": 500,
    "top_p": 0.90,
}
template = """You are a powerful text-to-SQL model. Your job is to answer questions about a database. You are given a question and context regarding one or more tables.

You must output the SQL query that answers the question.

### Input:
`{question}`

### Context:
`{context}`

### Response:
"""
prompt = PromptTemplate.from_template(template=template)
llm = SageMakerLLM(
    endpoint_name=os.getenv("SAGEMAKER_ENDPOINT_NAME"),
    model_kwargs=generation_args,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION_NAME"),
)


def main():
    st.set_page_config(page_title="7BSQL Master", page_icon="📊", layout="wide")
    st.title("7BSQL Master")

    col1, col2 = st.columns([2, 3])

    with col1:
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, encoding="latin1")
            df.columns = df.columns.str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
            st.write("Here's a preview of your uploaded file:")
            st.write(df.head())

            context = pd.io.sql.get_schema(df.reset_index(), "df").replace('"', "")
            st.write("SQL Schema:")
            st.code(context)

    with col2:
        if uploaded_file is not None:
            question = st.text_input("Write a question about the data", key="question")

            if st.button("Get Answer", key="get_answer"):
                if question:
                    input = {"context": context, "question": question}
                    formatted_prompt = prompt.invoke(input=input).text
                    stream = llm.stream_complete(formatted_prompt, formatted=False)
                    response_placeholder = st.empty()
                    response = ""
                    for r in stream:
                        response += r.delta
                        response_placeholder.code(response)
                    final = response.replace("`", "").replace("sql", "").strip()
                    st.write("Answer:")
                    try:
                        result = sqldf(final, locals())
                        st.write(result)
                    except Exception as e:
                        st.error(f"Error executing the SQL query: {str(e)}")
                else:
                    st.warning("Please enter a question before clicking 'Get Answer'.")


if __name__ == "__main__":
    main()
