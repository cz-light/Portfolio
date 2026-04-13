# Portfolio

A collection of personal and academic projects spanning systems programming, database design, and AI/ML applications.

---

## Projects

### VulnDetective
**Ethereum Smart Contract Vulnerability Detection**

A research project completed during a summer internship at Boise State University, investigating the use of large language models to detect vulnerabilities in Ethereum smart contracts.

- **Type:** Research / Internship
- **Collaborators:** Team project
- **Repository:** [LLM-SC-Vuln-Detection](https://github.com/tesessa/LLM-SC-Vuln-Detection) *(hosted separately)*

---

### EMTALA Legal Assistant
**RAG-Powered Chatbot for EMTALA Enforcement Cases**

A retrieval-augmented generation (RAG) chatbot that helps lawyers, physicians, and medical staff navigate HHS enforcement actions related to the Emergency Medical Treatment and Labor Act (EMTALA). The source data comes from the [HHS OIG Enforcement Actions page](https://oig.hhs.gov/fraud/enforcement/?type=emtalapatient-dumping&page=), which is difficult to search manually.

**Pipeline:**
1. **Data Collection** — Scrapes EMTALA case data from HHS OIG using `requests` and `BeautifulSoup`, outputting structured JSON with case metadata (hospital, state, penalty amount, date, etc.)
2. **Data Cleaning** — Manual review and normalization of AI-extracted metadata fields
3. **Vector Database** — Embeds and stores case documents in a persistent ChromaDB vector store using OpenAI embeddings
4. **Agent** — GPT-4o-mini powered agent that retrieves relevant case chunks and answers user queries with citations
5. **Web App** — Streamlit frontend for interactive querying

**Tech Stack:** Python, OpenAI API (GPT-4o-mini, embeddings), ChromaDB, Streamlit, BeautifulSoup, dotenv

**To Run:**
```bash
# Add a .env file to src/ with your OpenAI key:
# OPENAI_API_KEY=your_key_here

python src/main.py
```

---

### Tech Layoffs SQL Analysis
**Data Cleaning & Exploratory Analysis of Tech Industry Layoffs**

A end-to-end SQL project cleaning and analyzing a dataset of tech industry layoffs spanning late 2022 to early 2023. Built to practice real-world data preparation and exploratory analysis workflows using MySQL.

1. Cleaned raw data by standardizing formats, correcting country name inconsistencies, converting date strings to proper SQL DATE types, and removing uninformative null records
3. Explored trends across companies, industries, countries, and time using aggregations, CTEs, window functions, and rolling totals
   
**Key finding:** January 2023 saw a dramatic spike in layoffs, with the United States and Consumer/Retail industries accounting for the largest share of total layoffs

**Tech Stack:** MySQL, MySQL Workbench

---

### Video Game Sales Dashboard
**Interactive Tableau Dashboard for Global Video Game Sales Analysis**

An interactive Tableau dashboard exploring global video game sales trends across genres, platforms, and regions using a dataset of thousands of game titles spanning 1980–2020.

**Visualizations include:**

**Area chart —** Genre sales over time, showing the rise and decline of the industry with Action and Sports dominating the peak years around 2008–2009

**Dual bar chart —** Global sales vs. global sales minus EU by genre, highlighting the EU market's contribution across categories

**Bar chart —** Top 10 platforms by global sales, with PS2 leading all platforms

**Tech Stack:** Tableau Public, Kaggle Video Game Sales Dataset

[View Dashboard on Tableau Public](https://public.tableau.com/app/profile/cora.zeger/viz/VideoGameSalesDashboard_17761065420620/VideoGameSaleDashboard#2)

---

### Dash Transaction Database
**Synthetic Blockchain Transaction Database**

A relational database modeling Dash cryptocurrency transactions, built for a database management class to practice schema design, ER modeling, and SQL querying. Since no public Dash transaction database exists, synthetic data was generated to mimic real-world patterns.

**Schema includes:** Users, Blocks, Transactions, Masternodes

**Files:**
- `DASHdb.db` — SQLite database
- `tableCreationSQL` — DDL for the full schema
- `queries.txt` — Annotated sample queries for extracting insights and detecting anomalies
- `data/` — CSV source files used to populate the database

**Tech Stack:** SQLite, SQL, LucidChart (ER diagram)

---

### BasicShell
**Unix Shell Implemented in C**

A lightweight, Unix-like command-line shell written in C, built for a systems programming course to gain hands-on experience with process management, system calls, and I/O handling.

**Features:**
- Execute standard shell commands (`ls`, `ps`, etc.)
- Directory navigation with `cd`
- Input (`<`) and output (`>`) redirection
- Background process execution with `&`
- Clean exit with `exit`

**To Run:**
```bash
gcc -o basicshell BasicShell.c
./basicshell
```

**Tech Stack:** C, Unix system calls (`fork`, `exec`, `wait`, `dup2`)
