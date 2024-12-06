import re

import qdrant_client
from openai import OpenAI

from swarm import Bee
from swarm.repl import run_demo_loop

# Initialize connections
client = OpenAI()
qdrant = qdrant_client.QdrantClient(host="localhost")

# Set embedding model
EMBEDDING_MODEL = "text-embedding-3-large"

# Set qdrant collection
collection_name = "help_center"


def query_qdrant(query, collection_name, vector_name="article", top_k=5):
    # Creates embedding vector from user query
    embedded_query = (
        client.embeddings.create(
            input=query,
            model=EMBEDDING_MODEL,
        )
        .data[0]
        .embedding
    )

    query_results = qdrant.search(
        collection_name=collection_name,
        query_vector=(vector_name, embedded_query),
        limit=top_k,
    )

    return query_results


def query_docs(query):
    """Query the knowledge base for relevant articles."""
    print(f"Searching knowledge base with query: {query}")
    query_results = query_qdrant(query, collection_name=collection_name)
    output = []

    for i, article in enumerate(query_results):
        title = article.payload["title"]
        text = article.payload["text"]
        url = article.payload["url"]

        output.append((title, text, url))

    if output:
        title, content, _ = output[0]
        response = f"Title: {title}\nContent: {content}"
        truncated_content = re.sub(
            r"\s+", " ", content[:50] + "..." if len(content) > 50 else content
        )
        print("Most relevant article title:", truncated_content)
        return {"response": response}
    else:
        print("No results")
        return {"response": "No results found."}


def send_email(email_address, message):
    """Send an email to the user."""
    response = f"Email sent to: {email_address} with message: {message}"
    return {"response": response}


def submit_ticket(description):
    """Submit a ticket for the user."""
    return {"response": f"Ticket created for {description}"}


def transfer_to_help_center():
    """Transfer the user to the help center bee."""
    return help_center_bee


user_interface_bee = Bee(
    name="User Interface Bee",
    instructions="You are a user interface bee that handles all interactions with the user. Call this bee for general questions and when no other bee is correct for the user query.",
    functions=[transfer_to_help_center],
)

help_center_bee = Bee(
    name="Help Center Bee",
    instructions="You are an OpenAI help center bee who deals with questions about OpenAI products, such as GPT models, DALL-E, Whisper, etc.",
    functions=[query_docs, submit_ticket, send_email],
)

if __name__ == "__main__":
    run_demo_loop(user_interface_bee)
