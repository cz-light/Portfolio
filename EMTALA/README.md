Background:


Pipeline steps:

1) Pull in the data using the transformURLtoData.py
    * Libraries used: requests, bs4, openai, os, json
    * Input: Emtala fraud url
    * Output: Json document in the data foldar
    * Next steps for improvement:
        - scrape the archives and add the cases from before 2013 to the json
        - the cases with multiple webpages need to be combined in some way


2) Check over the data in the Json foldar
    * AI pulled in all possible values for the metadata, this needs to be checked
        - Check all none values
        - Combine continuous entries
        - If multiple metadata exist for one element, it needs to become a single value for the vector db
            * for money: choose the overall penalty amount, some include sub amounts that add up to the overall
            * for dates: choose the date the pentaly was awarded/case was closed
            * for hospital name: ensure only one exists, some cases are continuations of a previous paragraph-- these hospital names need to be entered
            * for hospital abbr: ensure only one exists
            * for state: ensure only one exists, if need be look up the hospital and assign the correct state
    * Next steps for improvement
        - include more metadata ie city, doctors, sub-penalty amounts if existant, patient symptoms/patient identification, emtala infraction, corporation/LLC

3) create vector db from the json data in createVectorDB.py
    * Libraries used: chromadb, os, openai, json
    * Input: Json document in the data folder
    * Output: Persistent chroma vector db in the .chroma_persistent_db foldar

4) create agent to query the vector db in agent.py
    * Libraries used: chromadb, os, openai, dotenv
    * Input: user query
    * Output: answer to user query with context from vector db



