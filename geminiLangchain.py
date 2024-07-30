# Step 1: Setup and Imports

import os
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.llms import GooglePalm  # We'll use this as a placeholder for Gemini
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain
import json

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDRJK5mRSBFq6u6Ip6Nw5pb9JDIJ01rZD4"

# Step 2: Load WikiSQL Dataset

def load_wikisql_data(file_path):
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]

train_data = load_wikisql_data('path_to_train.jsonl')
dev_data = load_wikisql_data('path_to_dev.jsonl')

# Step 3: Connect to SQLite Database

db = SQLDatabase.from_uri("WikiSQL/data/train.db")

# Step 4: Configure LangChain with Google Palm (placeholder for Gemini)

llm = ChatGoogleGenerativeAI(model="gemini-1.5" , temperature=0.1)  # Replace with Gemini when available

# Step 5: Create Prompt Template

prompt_template = """Given the following SQL tables:
{table_info}

Generate a SQL query to answer the following question:
{question}

SQL Query:"""

prompt = PromptTemplate(
    input_variables=["table_info", "question"],
    template=prompt_template
)

# Step 6: Create LangChain Pipeline

llm_chain = LLMChain(llm=llm, prompt=prompt)

# Step 7: Function to Generate SQL Query

def generate_sql_query(question, table_info):
    return llm_chain.run(table_info=table_info, question=question)

# Step 8: Function to Execute SQL Query

def execute_sql_query(query):
    chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    return chain.run(query)

# Step 9: Example Usage

# Assume we have table info and a question
table_info = """
CREATE TABLE example_table (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT
)
"""
question = "What is the average age of people in the table?"

# Generate SQL query
generated_query = generate_sql_query(question, table_info)
print(f"Generated Query: {generated_query}")

# Execute the query
result = execute_sql_query(generated_query)
print(f"Query Result: {result}")

# Step 10: Evaluation (Basic Example)

def evaluate_query(generated_query, reference_query):
    # This is a very basic evaluation. In practice, you'd want more sophisticated comparison.
    return generated_query.lower().strip() == reference_query.lower().strip()

# Assume we have a reference query
reference_query = "SELECT AVG(age) FROM example_table"
evaluation_result = evaluate_query(generated_query, reference_query)
print(f"Query Evaluation: {'Correct' if evaluation_result else 'Incorrect'}")