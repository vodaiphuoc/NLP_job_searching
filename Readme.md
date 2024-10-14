## For function 2
- **Task definition**: given a JobPostId, find the top-k suitable CVs for the job
- **Approach**: Using sentence embeddings model with training schema includes
	**supervised** and **unsupervised** training.
	For demo purpose, using a pre-trained sentence embeddings model (source = "https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html")
	For later stage of project, using **hybrid** of supervised and unsupervised training

- **Initialize Resume dataset**: source: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- **Initialize Job Posts dataset**: source https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset

- **Project processes**:
- a user (Job seeker), select 1 in 2 options:
1) input into UI -> DB
2) upload pdf (input2UI = Null) -> call api pdf_extractor (Python server)
-> return JSON data (with .Net)-> DB

- a backgroud job/worker: triggered by a POST api to Python server
for fine_tuning/compute similarity score (range from 0 to 1) -> DB

- a user (Recruiter or Job seeker) perform search:
	.Net perform query to target table in DB -> return results


## Table list
"Users", "SkillSets", "SeekerSkillSets, "Reviews", "JobTypes", "JobSkillSets", "JobPosts", "JobPostActivitys", "JobLocations", "ExperienceDetails", "EducationDetails", "Companys", "CVs", "BusinessStreams"

# How to use
- Create virtual environment in python (3.10)
python -m venv myenv
- To active myenv:
myenv\Scripts\activate
- To install all packages
pip install -r requirements.txt
- To create all tables, in psql run command:
\i path_to_create_tables.sql
- [Optional] To clear all tables in the database, in psql:
DROP SCHEMA public CASCADE;
- To insert demo data into the database, run:
python insert.py
- To get similarity score, run:
python single_run.py

## Ref psql command
1) \? list all the commands
2) \l list databases
3) \conninfo display information about current connection
4) \c [DBNAME] connect to new database, e.g., \c template1
5) \dt list tables of the public schema
6) \dt <schema-name>.* list tables of certain schema, e.g., \dt public.*
7) \dt *.* list tables of all schemas
8) Then you can run SQL statements, e.g., SELECT * FROM my_table;(Note: a statement must be terminated with semicolon ;)
9) \q quit psql



# Key learning resources:
- Word Embedding: represent each word seperately 
https://info216.wiki.uib.no/images/c/c4/IntroToWordEmbeddings.pdf 

- Transformer model: the rise of transformer archtecture for NLP tasks
https://huggingface.co/learn/nlp-course/chapter1/4

- Sentence embeddings: represent word, sentence, paragraph with contexts
https://huggingface.co/blog/getting-started-with-embeddings
