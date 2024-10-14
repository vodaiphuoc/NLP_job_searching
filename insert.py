import pandas as pd
import pathlib
from src.database import InsertDEMO2MainDB
db = InsertDEMO2MainDB()

# config paths
linkedjobs_folder_path = pathlib.Path("demo_data","linkedjobs","cleaned_data")
lvcr_resume_folder_path = pathlib.Path("demo_data,livecareer_resume_dataset,cleaned_data")

bus_stream_path = pathlib.Path(linkedjobs_folder_path,"busniess_steam.csv")
comp_data_path = pathlib.Path(linkedjobs_folder_path,"company_data.csv")
job_location_path = pathlib.Path(linkedjobs_folder_path,"JobLocation.csv")
skillsets_path = pathlib.Path(linkedjobs_folder_path,"SkillSets.csv") 
jobposts_path = pathlib.Path(linkedjobs_folder_path,"JobPosts.csv") 
jobskillsets_path = pathlib.Path(linkedjobs_folder_path,"JobSkillSets.csv") 


users_path = pathlib.Path(linkedjobs_folder_path,"Users_table.csv")
edu_detail_path = pathlib.Path(linkedjobs_folder_path,"TempEducationDetails_table.csv")
exp_detail_path = pathlib.Path(linkedjobs_folder_path,"ExperienceDetail_table.csv")
seeker_skills_path = pathlib.Path(linkedjobs_folder_path,"SeekerSkills_table.csv")
psa_path = pathlib.Path(linkedjobs_folder_path,"Position_Summary_Achievements_table.csv")


# insert processes
bus_stream = pd.read_csv(bus_stream_path, header=  0)
bus_stream = [bus_stream.iat[row,0] for row in range(len(bus_stream))]
db.insertBussinessStream(input_data= bus_stream)

comp_data = pd.read_csv(comp_data_path, header=0)
comp_data = [comp_data.iloc[row].to_dict() 
             for row in range(len(comp_data))]
db.insertCompanys(input_data= comp_data)

job_location = pd.read_csv(job_location_path, header= 0)
job_location = [job_location.iloc[row].to_dict() 
             for row in range(len(job_location))]
db.insertJobLocation(input_data= job_location)

db.insertJobTypes()

skillsets = pd.read_csv(skillsets_path, header=  0)
skillsets = [skillsets.iat[row,0]
             for row in range(len(skillsets))]
db.insertSkillSets(input_data= skillsets)


jobposts = pd.read_csv(jobposts_path, header=  0)
jobposts = [jobposts.iloc[row].to_dict()
             for row in range(len(jobposts))]
db.insertJobPosts(input_data= jobposts)


jobskillsets = pd.read_csv(jobskillsets_path, header=  0)
jobskillsets = [jobskillsets.iloc[row].to_dict()
             for row in range(len(jobskillsets))]
db.insertJobSkillSet(input_data= jobskillsets)


users = pd.read_csv(users_path, header=  0)
users = [str(users.iat[row,0])
             for row in range(len(users))]
db.insertUsers(input_data= users)


temp_edu_details = pd.read_csv(edu_detail_path, header=  0)
temp_edu_details = [temp_edu_details.iloc[row].to_dict()
             for row in range(len(temp_edu_details))]
db.insertEducationDetail(input_data= temp_edu_details)


exp_details = pd.read_csv(exp_detail_path, header=  0)
exp_details = [exp_details.iloc[row].to_dict()
             for row in range(len(exp_details))]
db.insertExperienceDetail(input_data= exp_details)

seeker_skills = pd.read_csv(seeker_skills_path, header=  0)
seeker_skills = [seeker_skills.iloc[row].to_dict()
             for row in range(len(seeker_skills))]
db.insertSeekerSkillSet(input_data= seeker_skills)


pos_sum_ach = pd.read_csv(psa_path, header=  0)
pos_sum_ach = [pos_sum_ach.iloc[row].to_dict()
             for row in range(len(pos_sum_ach))]
db.insertPositionSummaryAchievements(input_data= pos_sum_ach)


db.insertJobPostActivitys()


