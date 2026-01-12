"""
This script creates a persistent Chroma vector database using OpenAI embeddings
from EMTALA case data stored in a JSON file.
"""

from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import os
import chromadb.utils.embedding_functions as embedding_functions
import json



def format_metadata(metadata):
    #incoming metadata dict values are lists with single items or None, need to format them properly
    formatted_metadata = {
        "penalty": float(metadata["penalty"][0].replace(",","").replace("$","")) if metadata["penalty"][0] is not None else "None",
        "date": str(metadata["date"][0]) if metadata["date"][0] is not None else "None",
        "hospital_name": str(metadata["hospital_name"][0]) if metadata["hospital_name"][0] is not None else "None",
        "hospital_abbreviation": str(metadata["hospital_abbreviation"][0]) if metadata["hospital_abbreviation"][0] is not None else "None",
        "state": str(metadata["state"][0]) if metadata["state"][0] is not None else "None"
    }
    return formatted_metadata

def add_content_to_collection(collection):
    metadata = []
    ids = []
    content = []
    
    with open("data/emtala_case_data.json", "r") as f:
        emtala_case_data = json.load(f)

    #chroma db ids need to be unique strings
        #the metadata needs to be a list of dicts with the values being str, int, float, bool types
        #the documents need to be a list of strings
    #all three lists need to be the same length and correspond to each other by index
    for i in range(len(emtala_case_data)):
        ids.append(str(emtala_case_data[i]["id"]))
        metadata.append(format_metadata(emtala_case_data[i]["metadata"]))
        content.append(emtala_case_data[i]["paragraph"])

    collection.add(documents=content,metadatas=metadata,ids=ids)


def main():
    ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    #setup to be persistent so that we don't constantly embedd the same data over and over
    chroma_client = chromadb.PersistentClient(path='.chroma_persistent_db')

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=ai_client.api_key,
                    model_name="text-embedding-3-small"
                    #dimensions=512
            )
    #chroma_client.delete_collection(name="EMTALA_fulldata")  #uncomment to reset vector db during testing


    #check if vector db exists, if not then create it
    
    collection_names = [col.name for col in chroma_client.list_collections()]
    if "EMTALA_fulldata" in collection_names:
        print("Vector DB already exists. Skipping creation.")
        collection = chroma_client.get_collection(name="EMTALA_fulldata", embedding_function = openai_ef)
    else:
        print("Creating vector DB...")
        collection = chroma_client.create_collection(name="EMTALA_fulldata", embedding_function=openai_ef)
        add_content_to_collection(collection)
    
    return collection