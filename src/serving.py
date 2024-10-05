from typing import List



def find_CVs(JobPostId: int)-> List[str]:
    """
    Given an input id `JobPostId`, find most suitable CV urls
    """

    # using JobPostId to query `Application` table 
    # fields: id, JobPostId, UserId, ApplicationDate, Status, CVid


    ###### For job post data (requirements) #####
    # using JobPostId to query `JobPost` table
    # result: JobTitle, JD, ExperiencedRequired, 
    # QualicationRequired 



    # using JobPostId to query `JobSkillSet` table
    # result: SkillSetId, SkillLevelRequired




    # using JobPostId to query `SkillSet` table
    # result: SkillSetId, SkillLevelRequired




    ###### For user data #########################
    # using UserId to query `SeekerSkillSet` table
    # fields: UserId, SkillSetId, ProficiencyLevel




    # For SkillSet
    # using UserId to query `SeekerSkillSet` table
    # fields: UserId, SkillSetId, ProficiencyLevel




    # For SkillSet details
    # using SkillSetId to query `SkillSet` table
    # fields: Id, Name, Shorthand, Description, SkillLevel




    # For Experience
    # using UserId to query `ExperienceDetail` table
    # fields: Id, UserId, Position, StartDate, EndDate, Responsibilities, Archivements





    # For Education
    # using UserId to query `EducationDetail` table
    # fields: Id, UserId, Name, InsitutionName, Degree, FieldOfStudy, StartDate, EndDate, GPA


    return None


class Serving_Class(object):
    def __init__(self) -> None:
        pass