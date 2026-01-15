Background:
- there is no public database of Dash transactions, making it difficult to analyze spending patterns or detect anomalies, so for a database management class project, I created a Dash transaction database that can be queried for various insights
- currently, the database contains synthetic data generated to mimic real-world Dash transactions. The data can be found in the data folder

File Description:
- DASHdb.db - the main database file containing the Dash transaction data in my implementation of the schema
- queries.txt - a text file containing sample SQL queries that can be run against the database to extract insights; these queries contain comments explaining their purpose and expected results
- tableCreationSQL - a file containing the SQL commands used to create the database schema, including table definitions and relationships

Project Steps:
1. created a schema and then ER diagram to model Dash transactions, users, and related entities
    * lucidchart was used to create the ER diagram
    * the schema includes tables for users, blocks, dash transactions, and the masternodes
    * Steps for improvement:
        - more research into real-world Dash transaction patterns to better inform the schema design

2. implemented the database using SQL
    * sqlLite was used to implement the database schema
    * created tables, relationships, and constraints based on the ER diagram
    * Steps for improvement:
        - optimize table structures and indexing for better query performance

3. generated synthetic data to populate the database
    * chatgpt was used to help generate realistic synthetic data for Dash transactions, users, and blocks
    * I used sqlLite to import the data
    * Steps for improvement:
        - use real-world data to create a more accurate and comprehensive database