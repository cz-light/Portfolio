"""
This script serves as the entry point for the EMTALA Legal Assistant application.
To run, ensure your in the EMTALA directory and execute: streamlit run src/main.py
"""
import json
import transformURLtoData
import createVectorDB
import webapp

with open("data/emtala_case_data.json", "r") as f:
    emtala_case_data = json.load(f)

if __name__ == "__main__":
    print("\nStarting data extraction process...")
    if not emtala_case_data:
        transformURLtoData.main()
        with open("data/emtala_case_data.json", "r") as f:
            emtala_case_data = json.load(f)
    else:
        print("Data already exists. Skipping extraction.")
    print("Data extraction process completed.")
    print(f"Total cases extracted: {len(emtala_case_data)}\n")

    #the vector db creation is checked/handled inside createVectorDB.main()
    print("Creating vactor database...")
    collection = createVectorDB.main()
    print("Vector database creation completed.")
    print(f"Total cases in database: {collection.count()}\n")

    print("Launching EMTALA Legal Assistant application...")
    webapp.main(collection)