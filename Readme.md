input query:  tiếng anh + tiếng việt (this factor influences tokenizer)

1) **Introduction**
	**Fucntion 1**: using NLP model for improving job search experience of users.
	Given a user query input search which describes what they looking for, the model output SQL query for the database then the system returns most potential job posts for the user.
	**Function 2**: using NLP model for improving CV search of HRs (*process later*)
1) **Related works**
2) **Methods** 
	1) using text2sql model:  (for writing word only)
		**Basic knowledge requried**:
		 - How to training a normal Deep neuron network using Pytorch
		 - Typical components in a Transformer based model in NLP (embedding layers, transformer blocks,etc...) + tokenizer. What are type of embedding layers in above model?
		 - How to train and Transformer based model for seq2seq ( sequence to sequence) task. What is loss function and metric can be used in this case?
	1) using embedding model (*process later*)
3) **Data curation**
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
		- JD:
		- Job_requirement_detail: str
		- Benefits: str
		After cleaning data, we will have one table only contains job posts
		
	3) *Create queries for each job posts*
		Some possible to create queries:
		- Using LLM
		- create using if/else
		- combine boths

4) Experiment and results
	Run training the model with created data
5) References

