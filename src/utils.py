# from typing import List, Tuple

# # related to jobposts
# def insertBussinessStream(BusinessStreamName:str):

#     {
#         "Id"	
#         "BusinessStreamName": BusinessStreamName,
#         "Description": ""	
#         "CreatedDate"
#         "ModifiedDate"	
#         "CreatedBy"
#         "ModifiedBy"	
#         "IsDeleted"
#     }

# def insertCompanys():
#     {
#         "Id"	
#         "CompanyName"	
#         "CompanyDescription"	
#         "WebsiteURL"	
#         "EstablishedYear"
#         "Country"	
#         "City"	
#         "Address"	
#         "NumberOfEmployees"	
#         "BusinessStreamId"	
#         "CreatedDate"	
#         "ModifiedDate"	
#         "CreatedBy"	
#         "ModifiedBy"	
#         "IsDeleted"
#     }



# 'Experience', 'Qualifications', 'Salary Range', 'location',
#        'Country', 'Work Type', 'Company Size',
#        'Job Posting Date', 'Preference', 'Contact Person', 'Contact',
#        'Job Title', 'Role', 'Job Portal', 'Job Description', 'Benefits',
#        'skills', 'Responsibilities',

# def insertJobLocation(self, input_data: List[Tuple[str]])->None:
#     """
#     Insert many into 'JobLocation' table
#     Arg:
#         - input_data: List of Tuple of str
#     Exmaple: [(location, city), ...]
#     Note: location == city
#     Need to remove:
#         - "District"
#         - "PostCode"
#         - "State"
#         - "StressAddress"
#         - "CreatedDate"
#     """

#     insert_data = [
#         {
#         "District": "empty",
#         "City": location,
#         "PostCode": "empty",
#         "State":"empty",	
#         "Country": city,
#         "StressAddress":"empty"
#         # "CreatedDate": ,
#         # "ModifiedDate"	
#         # "CreatedBy"	
#         # "ModifiedBy"	
#         # "IsDeleted"
#         } 
#     for (location, city) in input_data]


#     try:
#         query = f"INSERT INTO JobLocations (information) VALUES (%s);"
#         cur.executemany(query, batch)
#     except:
#         print(f"Can't insert many into {target_table} table in the database!")


#     return None



# def insertJobType():
#     {
#     "Id"	
#     "Name"	
#     "Description"
#     }


# def insertSkillSets():
#     {
#     "Id"	
#     "ProficiencyLevel"	
#     "UserId"	
#     "SkillSetId"	
#     "CreatedDate"	
#     "ModifiedDate"	
#     "CreatedBy"	
#     "ModifiedBy"	
#     "IsDeleted"
#     }

# def insertJobSkillSet():
#     {
#         "Id"
#         "SkillSetId"	
#         "JobPostId"	
#         "CreatedDate"	
#         "ModifiedDate"	
#         "CreatedBy"	
#         "ModifiedBy"	
#         "IsDeleted"
#     }


# def insertJobPosts():

#     {
#         "JobTitle":,	
#         "JobDescription":,
#         "Salary":,	
#         "PostingDate":,	
#         "ExpiryDate":,	
#         "ExperienceRequired":,	
#         "QualificationRequired":,	
#         "ImageURL":,	
#         "SkillLevelRequired":,	
#         "Benefits":,
#         "IsActive":,
#         "UserId":,
#         "JobTypeId":,	
#         "CompanyId":,	
#         "JobLocationId":,	
#         "CreatedDate":,	
#         "ModifiedDate":,	
#         "CreatedBy":,
#         "ModifiedBy":,
#         "IsDeleted":,

#     }




# # related to Resume
# def insertUsers():

# {
#     "Id":,
#     "UserName":,
#     "PasswordHash":,
#     "PasswordSalt":,
#     "FirstName":,
#     "LastName":,
#     "Email":,
#     "PhoneNumber":,
#     "Role":,
#     "CompanyId":,
#     "CreatedDate":,
#     "ModifiedDate":,	
#     "CreatedBy":,
#     "ModifiedBy":,
#     "IsDeleted":,
# }

# def insertEducationDetail():
# {
#     "Id":,	
#     "Name":,	
#     "InstitutionName":,
#     "Degree":,
#     "FieldOfStudy":,
#     "StartDate":,
#     "EndDate":,
#     "GPA":,
#     "UserId":,	
#     "CreatedDate":,
#     "ModifiedDate":,
#     "CreatedBy":,
#     "ModifiedBy":,
#     "IsDeleted":,
# }



# def insertCVs():

#     {
#         "Id":,
#         "Url":,
#         "UserId":,
#     }



# def insertExperienceDetail():
#     {
#         "Id":,	
#         "CompanyName":,
#         "Position":,
#         "StartDate":,
#         "EndDate":,	
#         "Responsibilities":,
#         "Achievements":,	
#         "UserId":,
#         "CreatedDate":,
#         "ModifiedDate":,
#         "CreatedBy":,
#         "ModifiedBy":,	
#         "IsDeleted":,
#     }


# def insertSeekerSkillSet():
#     {
#         "Id":,
#         "ProficiencyLevel":,
#         "UserId":,
#         "SkillSetId":,
#         "CreatedDate":,	
#         "ModifiedDate":,	
#         "CreatedBy":,
#         "ModifiedBy":,	
#         "IsDeleted":,
#     }

# def insertJobPostActivitys():
#     {
#         "Id"	
#         "ApplicationDate"	
#         "Status"	
#         "UserId"	
#         "JobPostId"	
#         "CvId"	
#         "CreatedDate"	
#         "ModifiedDate"	
#         "CreatedBy"	
#         "ModifiedBy"	
#         "IsDeleted"
#     }