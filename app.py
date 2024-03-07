import asyncio

from dotenv import load_dotenv

load_dotenv()
import os
from operator import itemgetter

import pandas as pd
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pandasql import sqldf

template = """You are a powerful text-to-SQL model. Your job is to answer questions about a database. You are given a question and context regarding one or more tables.

You must output the SQL query that answers the question. You must put double quotes around the column names but not around the table name.

### Input:
`{question}`

### Context:
`{context}`

### Response:
"""
prompt = PromptTemplate.from_template(template=template)
llm = ChatOpenAI(
    model="gpt-4-0125-preview",
    temperature=0.3,
)
chain = (
    {"context": itemgetter("context"), "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)


async def main():
    st.set_page_config(page_title="7BSQL Master", page_icon="📊", layout="wide")
    st.title("7BSQL Master")

    col1, col2 = st.columns([2, 3])

    with col1:
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, encoding="latin1")
            st.write("Here's a preview of your uploaded file:")
            st.write(df.head())

            context = pd.io.sql.get_schema(df.reset_index(), "df")
            st.write("SQL Schema:")
            st.code(context)

    with col2:
        if uploaded_file is not None:
            question = st.text_input("Write a question about the data", key="question")

            if st.button("Get Answer", key="get_answer"):
                if question:
                    output = {"context": context, "question": question}
                    stream = chain.astream(output)
                    response_placeholder = st.empty()
                    response = ""
                    async for token in stream:
                        response += token
                        response_placeholder.code(response)

                    final = response.replace("```", "").replace("sql", "").strip()
                    st.write("Answer:")
                    try:
                        result = sqldf(final, locals())
                        st.write(result)
                    except Exception as e:
                        st.error(f"Error executing the SQL query: {str(e)}")
                else:
                    st.warning("Please enter a question before clicking 'Get Answer'.")


if __name__ == "__main__":
    asyncio.run(main())
