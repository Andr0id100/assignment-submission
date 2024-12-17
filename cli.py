import google.generativeai as genai
import os
import sqlite3
import re
from prompts import (
    database_metadata,
    query_generation_prompt_template,
    answer_prompt_template,
    relevany_check_prompt,
    question_rewrite_template,
)
from rich.console import Console
from rich.markdown import Markdown
from profanity_check import predict as is_profane
import argparse

import logging
from logging import getLogger

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="gemini-1.5-flash")
parser.add_argument("--db_path", type=str, default="database.db")
parser.add_argument("--indirect_mode", type=bool, default=False)

parser.add_argument("--verbose", type=bool, default=False)
args = parser.parse_args()

console = Console()

logging.basicConfig(level=logging.INFO if not args.verbose else logging.DEBUG)
logger = getLogger(__name__)


# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(args.model)

conn = sqlite3.connect(args.db_path)
cursor = conn.cursor()

while True:
    question = input("Question: ")

    if is_profane([question])[0]:
        logger.warning("Question contains profanity")
        continue

    response = model.generate_content(
        relevany_check_prompt.format(
            question=question, database_metadata=database_metadata
        )
    )

    if response.text.strip() == "Irrelevant":
        logger.warning("Question not relevant")
        continue

    if args.indirect_mode:
        response = model.generate_content(
            question_rewrite_template.format(
                question=question, database_metadata=database_metadata
            )
        )
        question = response.text

    response = model.generate_content(
        query_generation_prompt_template.format(
            database_metadata=database_metadata, question=question
        )
    )

    pattern = r"```sql\s+(.*?)\s+```"
    sql_query = re.search(pattern, response.text, re.DOTALL).group(1)
    logger.info(sql_query)

    cursor.execute(sql_query)
    results = cursor.fetchall()

    response = model.generate_content(
        answer_prompt_template.format(
            question=question, sql_query=sql_query, results=results
        ),
    )

    for chunk in response:
        md = Markdown(chunk.text)
        console.print(md, end="")

    print("=" * 50)
