from configparser import ConfigParser
from typing import Dict, Literal, List, Tuple, Union, Any
import psycopg2
from datetime import datetime, timedelta

class DB_Handling_Base(object):
    def __init__(self, 
                 config_file_path: str = "src/db.ini", 
                 section:str = "demo") -> None:
        self.config = self._get_DB_config(config_file_path = config_file_path, 
                                          section = section)

    def _get_DB_config(self, config_file_path:str, section:str)->Dict:
        parser = ConfigParser()
        parser.read(config_file_path)
        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, config_file_path))
        return config

    def _get_cursor_and_connection(self):
        try:
        # connecting to the PostgreSQL server
            conn = psycopg2.connect(**self.config)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

        cur = conn.cursor()
        return conn, cur

class TestDB_Handling(DB_Handling_Base):
    def __init__(self, config_file_path: str = "src/db.ini", section: str = "demo") -> None:
        super().__init__(config_file_path, section)
    
    # create tables
    def create_tables(self, table_name_list: List[Literal["resume", "jobpost","score"]])->None:
        """
        Primary key is set to type SERIAL so it can auto-increase
        """
        conn, cur = self._get_cursor_and_connection()
        for table_name in table_name_list:
            try:    
                prim_key_col_name = "CV_Id" if table_name == "resume" else "JobPostId" if table_name == "jobpost" else "Id"
                information = "information VARCHAR(39000)" if table_name != "id" else ""
                cv_job = ", CV_Id INTEGER, JobPostId INTEGER" if table_name =="id" else ""
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({prim_key_col_name} SERIAL PRIMARY KEY,{information}{cv_job});"
                cur.execute(query)
            except:
                print(f"Can't create {table_name} table in the database!")

        conn.commit()
        conn.close()
        cur.close()

    # insert data
    def insert(self, 
               target_table: Literal["resume", "jobpost", "score"],
               insertion_data: List[Tuple[str]],
               insert_batch_size = 1000
               )->None:
        """
        Insert many data into the database
        Example of `insertion_data`: [("some_string", ),("another string",)]
        Expect data in `insert_batch_size` is cleaned.
        """
        conn, cur = self._get_cursor_and_connection()

        # check if is correct type List of Tuple or not
        if not isinstance(insertion_data[0], Tuple):
            insertion_data = [(data,) for data in insertion_data]

        # split data into smaller chunks
        if len(insertion_data) > insert_batch_size:
            num_batch = len(insertion_data)//insert_batch_size
            batchs = [insertion_data[batch_id*insert_batch_size: (batch_id+1)*insert_batch_size] 
                        for batch_id in range(num_batch)
                        ]

        # branch for `resume` and `jobpost` table
        if target_table != "score":
            for batch in batchs:
                try:
                    query = f"INSERT INTO {target_table} (information) VALUES (%s);"
                    cur.executemany(query, batch)
                except:
                    print(f"Can't insert many into {target_table} table in the database!")
        
        # branch for `resume` and `jobpost` table
        else:
            for batch in batchs:
                try:
                    query = f"INSERT INTO {target_table} (CV_Id, JobPostId) VALUES (%s);"
                    cur.executemany(query, batch)
                except:
                    print(f"Can't insert many into {target_table} table in the database!")

        conn.commit()
        conn.close()
        cur.close()

    def delete_tabel(self,target_table: Literal["resume", "jobpost", "score"]):
        conn, cur = self._get_cursor_and_connection()
        
        query = f"DROP TABLE {target_table}"
        cur.execute(query)

        conn.commit()
        conn.close()
        cur.close()

    # def select(self, target_table:str, target_colums: List[str]):


class InsertMany2MainDB(DB_Handling_Base):
    def __init__(self,
                 config_file_path: str = "src/db.ini", 
                 section: str = "local"
                 ) -> None:
        super().__init__(config_file_path, section)

    # related to jobposts
    def insertBussinessStream(self, input_data: List[str])->None:
        """
        Insert many into 'BusinessStreams' table
        Arg:
            - input_data: List of Tuple of str
        Exmaple: [BusinessStreamName, ...]
        """
        conn, cur = self._get_cursor_and_connection()
        try:
            query = f'INSERT INTO public."BusinessStreams" \
                ("BusinessStreamName", "Description", "IsDeleted") \
                    VALUES (%s, %s, %s);'
            input_data = tuple([(data,"empty","false") for data in input_data])
            cur.executemany(query, input_data)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into BusinessStreams table\
                   in the database!.Error: {error}")
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertBussinessStream")
        return None

    def insertCompanys(self, input_data: List[Dict[str,Any]])->None:
        """
        Insert many into 'Companys' table
        Arg:
            - input_data: List of Dict with key is str, value is Any dtype
        Exmaple: [{'Industry':...,'Company Name':...}, ...]
        """
        conn, cur = self._get_cursor_and_connection()
        try:
            for data in input_data:
                for k,v in data.items():
                    if isinstance(v,str):
                        if "'" in v:
                            data[k] = v.replace("'","''")
                query = """INSERT INTO public."Companys" ("CompanyName", "CompanyDescription", 
                                                            "WebsiteURL", "EstablishedYear", 
                                                            "Country", "City", 
                                                            "Address", "NumberOfEmployees",
                                                            "BusinessStreamId", "IsDeleted")
                        VALUES ('{}', 'empty','{}', 2010,'{}','{}', 'empty', '{}',
                                (SELECT "Id" FROM public."BusinessStreams" 
                                WHERE public."BusinessStreams"."BusinessStreamName" = '{}')
                                ,'f');""".format(data["company_name"], data["Website"],
                                        data["State"],data["City"],
                                        data["Company Size"],data["Industry"])

                cur.execute(query)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into Companys table in the database! Error: ",error)
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertCompanys")
        return None


    def insertJobLocation(self, input_data: List[Dict[str, Any]])->None:
        """
        Insert many into 'JobLocation' table
        Arg:
            - input_data: List of Tuple of str
        Exmaple: [{'location':..., 'Country':...}, ...]
        Note: location means city
        """
        conn, cur = self._get_cursor_and_connection()

        try:
            input_data = [("empty", data["location"], "empty", "empty", data["Country"], "empty", "f") 
                          for data in input_data]
            query = f'INSERT INTO public."JobLocations" ("District", "City", \
                                                        "PostCode", "State", \
                                                        "Country", "StressAddress",\
                                                        "IsDeleted") \
                    VALUES (%s, %s, %s, %s,%s, %s, %s);'
            cur.executemany(query, input_data)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into JobLocations table in the database!", error)
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertJobLocation")
        return None

    def insertJobTypes(self)->None:
        """
        Possible for JobType is: 'Intern', 'Temporary', 'Full-Time', 
        'Contract', 'Part-Time'
        """
        conn, cur = self._get_cursor_and_connection()

        input_data = [('Intern','This position is mainly for undergraduate or recently graduate student',), 
                      ('Temporary','Only work for a short and determined period of time',),
                      ('Full-Time','This position work mainly 8 hours a day and 40 hours per week',), 
                      ('Contract','There is a contract between jobseeker and the company', ), 
                      ('Part-Time','Worker can work with 4-hour shift and many shifts in a week',)
                      ]
        
        try:
            query = f'INSERT INTO public."JobTypes" ("Name", "Description") VALUES (%s, %s);'
            cur.executemany(query, input_data)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into JobTypes table in the database!", error)
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertJobTypes")
        return None

    def insertSkillSets(self, input_data: List[str])->None:
        """
        Insert many into 'SkillSets' table
        Arg:
            - input_data: List of Tuple of str
        Exmaple: [(skill_1), (skill_2), ...]
        """
        conn, cur = self._get_cursor_and_connection()
        try:
            input_data = [(data,data,"empty","f") for data in input_data]
            query = f'INSERT INTO public."SkillSets" ("Name", "Shorthand", \
                                                    "Description", "IsDeleted") \
                        VALUES (%s,%s,%s,%s);'
            cur.executemany(query, input_data)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into SkillSets table in the database!", error)
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertSkillSets")
        return None

    def insertJobPosts(self, input_data: List[Dict[str,Any]])->None:
        """
        Insert many into 'JobPosts' table
        Arg:
            - input_data: List of Tuple of str
        Exmaple: [{'JobTitle':..., 'JobDescription':..., 'Salary':..., 'PostingDate':..., 
                    'ExperienceRequired':..., 'QualificationRequired':..., 'Benefits'...,  
                    }, 
                  (JobTitle_2,..,), 
                  ...
                  ]
        """
        conn, cur = self._get_cursor_and_connection()
        
        # prepare Ids state
        for data in input_data:
            for k,v in data.items():
                if isinstance(v,str):
                    if "'" in v:
                        data[k] = v.replace("'","''")

        
        for data in input_data:
            try:
                # insert state
                insert_query = """INSERT INTO public."JobPosts" ("JobTitle", "JobDescription", 
                                                            "Salary", "PostingDate", "ExpiryDate",
                                                            "ExperienceRequired", "QualificationRequired", 
                                                            "SkillLevelRequired", "Benefits", "IsActive",
                                                            "JobTypeId", "CompanyId", "JobLocationId",
                                                            "IsDeleted")
                        VALUES ('{}','{}','{}', '{}','{}','{}','{}', 3,'{}','t','{}','{}','{}','f');
                                """.format(data["Job Title"], data["Job Description"],
                                        data["Salary Range"],
                                        datetime.strptime(data["Job Posting Date"], "%Y-%m-%d"),
                                        datetime.now() + timedelta(days= 45),
                                        data["Experience"],data["Qualifications"], data["Benefits"],
                                        data["Work Type Id"], data["Company Id"], data["JobLocation Id"]
                                        )

                cur.execute(insert_query)
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"Can't insert many into JobPosts table in the database! Error: ",error)
            
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertJobPosts")
        return None

        

    def insertJobSkillSet(self, input_data: List[Tuple[str]]):
        """
        Insert many into 'JobSkillSets' table
        Arg:
            - input_data: List of Tuple of str
        Exmaple: [(JobPostId_1,SkillSetId_1), (JobPostId_2,SkillSetId_2), ...]
        """
        conn, cur = self._get_cursor_and_connection()
        try:
            input_data = [(data["JobPostId"], data["SkillSetId"],"f") for data in input_data]
            query = f'INSERT INTO public."JobSkillSets" ("JobPostId", "SkillSetId","IsDeleted") \
                        VALUES (%s,%s,%s);'
            cur.executemany(query, input_data)
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Can't insert many into JobSkillSets table in the database!", error)
        
        conn.commit()
        conn.close()
        cur.close()
        print("Done insertJobSkillSet")
        return None


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