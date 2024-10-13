input query:  tiếng anh + tiếng việt (this factor influences tokenizer)

1) **Introduction**
	**Fucntion 1**: using NLP model for improving job search experience of users.
	Given a user query input search which describes what they looking for, the model output SQL query for the database then the system returns most potential job posts for the user.
	**Function 2**: using NLP model for improving CV search of HRs (*process later*)
	- keyword extraction
	- sentence emebddings
	
2) **Related works**


3) **Methods** 
	1) using text2sql model:  (for writing word only)
		**Basic knowledge requried**:
		 - How to training a normal Deep neuron network using Pytorch
		 - Typical components in a Transformer based model in NLP (embedding layers, transformer blocks,etc...) + tokenizer. What are type of embedding layers in above model?
		 - vocalbulary size ? -> word embedding size

		 - How to train and Transformer based model for seq2seq ( sequence to sequence) task. What is loss function and metric can be used in this case?
		 - Normal flow (in Pytorch):
		 	- Load dataset
			- setup tokenizer
			- class My_Dataset(torch.utils.data.Dataset):
				def __init__

				def __len__

				def _getitem__(self, index):
					# tokenizer
					return 1 query (user input)  + 1 SQL query

			- loader = torch.utils.data.Loader(My_Dataset())

			- define model: Bert

			- loss function + optimizer Adam

			- training loop:
			for query, sql in loader:
				predict_sql = model(query)
				loss_value = loss_fn(sql, predict_sql)

				loss_value.backward() # calculate gradient

				optimizer.step()  # new_weight = old_weight + learning_rate*gradient
		

	1) using embedding model (*process later*)

4) **Data curation**
	1) *Format data*
	To reduce the **complexity of output SQL query**, most important columns are gatherd into one target table namely "NLP_search" for this functionality (this data is queried/created from all possibel tables of the website), target columns:
	- Job_id (main output of SQL query), Job title, salary, experienceRequired, qualificationRequired, SkillLevelRequired, benefits, companyName
	Some columns like ExpiryDate or isActive maby embedded into output SQL query with defaults like ExpiryDate's value has always after current day and isActive's value is alwasy True since this is what expect from every users.

	2) *Prepare job posts data*: crawl or select job post data with about target columns from job search website in order to filling data in Postgre database
		Target websites: jobsgo.vn
		Get job_list in ["ke-toan-kiem-toan", "tai-chinh-ngan-hang", "hanh-chinh-van-phong", "kinh-doanh-ban-hang", "marketing", "xay-dung", "it-phan-mem", "hanh-chinh-van-phong"] : Done
		Get data in each job post: 50%
		Field list: 
		- job_type: str, part-time or full-time
		- position/level: str
		- degreeRequired: str
		- ExperimentRequired: str
		- PostDate:
		- AgeRequired: str
		- JobDomain: 
		- Skills
		- Location
		- JD: str
		- Job_requirement_detail: str
		- Benefits: str
		After cleaning data, we will have one table only contains job posts
		
	3) *Create queries for each job posts*
		Some possible to create queries:
		- Using LLM
		- create using if/else
			- 10 fields
			- each field: n Unique values

			- 10 cases: 1 field, 2 fields, ... 10 fields
				1 field: 1C10 cases [field_1, field_3, ...]
				2 field: 2C10 cases [(field_1, field_2), ..., (field_3, field_9)]
				3 field: 3C10 cases [(field_1, field_4), ..., (field_8, field_6)]
				...
				10 field: 10C10 cases


def create(field_name:str, unique_values: List[str]):

	sign_dict = {"greater":">", "equal":"==", "less than": "<"}

	for each_unique_value in unique_values:
		sql_query_out = 
		"""
			SELECT * WHERE {column_name} {sign} {VALUE} <- unique value
		"""
		sql_query_out.format_map({column_name = field_name, VALUE = each_unique_value})


		for sign in :
		user_query = f"I want to find job with {field_name} related to each_unique_value"



5) Experiment and results
	Run training the model with created data
6) References




## For function 2
- **Task definition**: given a JobPostId, find the top-k suitable CVs for the job
- **Approach**: Using sentence embeddings model with training schema includes
	**supervised** and **unsupervised** training.
	For demo purpose, using a pre-trained sentence embeddings model (source = "https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html")
	For later stage of project, using **hybrid** of supervised and unsupervised training

- **Initialize Resume dataset**: source: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- **Initialize Job Posts dataset**: source https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset
- **Initialize JSON Resume dataset**: https://huggingface.co/datasets/Mehyaar/Annotated_NER_PDF_Resumes

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


1) training model+ assign score (oFFLINE)


2) upload pdf CV -> model -> insert db (online)


3) (online), inference time = serach time
input

jobpostID

-> top-k 5 cv_id

input

userID + cv_id

-> top-k 5 jobpost_id


