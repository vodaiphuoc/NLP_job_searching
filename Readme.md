## For function 2
- **Task definition**: given a JobPostId, find the top-k suitable CVs for the job
- **Approach**: Using sentence embeddings model with training schema includes
	**supervised** and **unsupervised** training.
	For demo purpose, using a pre-trained sentence embeddings model (source = "https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html")
	For later stage of project, using **hybrid** of supervised and unsupervised training

- **Initialize Resume dataset**: source: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- **Initialize Job Posts dataset**: source https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset

- **Project processes**:
	1) With **Admin** role: training/fine-tuning the model
		- Pre-pare dataset: perform query data from list of tables to form the target training
		dataset
		- Run training process and get results
		- Compare models
		- **Permission** to use the trained model to compute similarity between job posts and CVs and
		assign to database (a seperate table named "Sim_score" table). Its highlight that the process of calculate similarity can be done in offline process which is not perform when user do query search which **reduce** inference time
	
	2) With user (Recruiter and Job seeker) role:
		- when user input (JobPostID for recruiters or userId for job seekers), perform search in table "Sim_score" table to archive
		top-k highest similarity score

## psql command
1) \? list all the commands
2) \l list databases
3) \conninfo display information about current connection
4) \c [DBNAME] connect to new database, e.g., \c template1
5) \dt list tables of the public schema
6) \dt <schema-name>.* list tables of certain schema, e.g., \dt public.*
7) \dt *.* list tables of all schemas
8) Then you can run SQL statements, e.g., SELECT * FROM my_table;(Note: a statement must be terminated with semicolon ;)
9) \q quit psql


## Table list
"Users", "SkillSets", "SeekerSkillSets, "Reviews", "JobTypes", "JobSkillSets", "JobPosts", "JobPostActivitys", "JobLocations", "ExperienceDetails", "EducationDetails", "Companys", "CVs", "BusinessStreams"

To create all tables, in psql run command:
\i path_to_create_tables.sql
[Optional] To clear all tables in the database, in psql:
DROP SCHEMA public CASCADE;
To insert demo data into the database, run:
python insert.py