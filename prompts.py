database_metadata = """
Table: conversations
- id (INTEGER PRIMARY KEY)
  - Unique identifier for each conversation
  - Auto-incrementing
- text (TEXT)
  - Stores the full text of a conversation

Table: features
- conversation_id (INTEGER)
  - Foreign key referencing conversations(id)
- tag (TEXT)
  - Tag associated with a conversation with information pertaining to what the conversation is about
- user_final_sentiment (TEXT)
  - The final sentiment of the user. One of Positive, Negative, Neutral or Not Enough Information.
- Relationship: Many-to-One with conversations

Table: distilled
- conversation_id (INTEGER)
  - Foreign key referencing conversations(id)
- key_issue (TEXT)
  - Stores a distilled version of the issue that the user had
- key_resolution (TEXT)
  - Stores a distilled version of the resolution provided by the support agent
"""


query_generation_prompt_template = """
Objective
You are an expert SQL query generator tasked with creating precise SQLite database queries that directly answer a specific question using provided database metadata.
Input Format

QUESTION: {question}
DATABASE_METADATA: Structured information about the database schema: \n{database_metadata}

Requirements for SQL Query Generation

Carefully analyze the question and database metadata
Identify the most relevant tables and columns for answering the question
Construct a query that:

Directly addresses the specific information requested
Uses appropriate JOIN operations if multiple tables are involved
Applies precise WHERE, GROUP BY, or HAVING clauses as needed
Handles any aggregations, filtering, or sorting requirements


Ensure the query is:

Efficient
Readable
Free of unnecessary complexity


Include comments explaining the query's logic if the query is complex
"""


answer_prompt_template = """
Objective: Generate a concise, informative answer to the following database query

Input:
- Question: {question}
- SQL Query: {sql_query}
- Query Results: {results}

Instructions:
1. Analyze the query results
2. Craft a precise, direct response that:
   - Directly answers the original question
   - Summarizes key insights from the data
   - Uses markdown formatting
   - Includes lists if multiple points are relevant
3. Constraints:
   - Focus only on information directly related to the question
   - Exclude any additional suggestions or commentary
   - Ensure the answer is clear and easily understood
"""

relevany_check_prompt = """Classify the following question as Relevant or Irrelevant to a quantitative question-answering system involving conversations between customers and support agents with data being stored in a database with the following metadata. \nMetadata: {database_metadata} Only respond with 'Relevant' or 'Irrelevant'. Question: {question}"""

question_rewrite_template = """
Based on the given question and the database metadata, rewrite the question to better aligned and more direct with what's available from the data. Just respond with the final version of the question.
Question: {question}
Database Metadata: {database_metadata}
"""