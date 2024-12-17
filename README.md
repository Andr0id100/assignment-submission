# Assignment Submission for NLP

## Data Enrichment
* Sentiment Extraction: Classify user sentiment as Positive, Negative and Neutral. Useful for queries where we want to improve customer experience.
* Tag Update: Even though the provided tags had wide converage, they seemed insufficient for certain topics like delivery issues. Added some additional granuality.
* Conversation Distillation: Reduced the conversation to a key issue stated by the user and a key resolution provided by the customer support agent. This works as additional metadata over tags that can be useful while querying for specific problems.
* Also tested some other approaches like entity extraction but the signal to noise ratio seemd to be lower in those methods.


## Question Answering Systems
* Checks for profanity and relevance for the question
* Generates an sql query for the question based on the schema for the database
* Uses the query results to create a condensed answer for the user questions.
* Also added an indirect mode for more vaugue questions, which rewrites the question to be more grounded in the available data.

Note: All the PII from the users seems to already be redacted from the dataset so that module wasn't implemented.

To run:
```bash
python cli.py
```

For the indirect model:
```bash
python cli.py --indirect_mode True
```
