-- Primary key needs SERIAL datatype to be auto-increment
CREATE SCHEMA public;

CREATE TABLE public."Users" (
  "Id"  SERIAL NOT NULL,
  "UserName" text NOT NULL,
  "PasswordHash" bytea  NULL, -- NOT NULL TO NULL
  "PasswordSalt" bytea  NULL, -- NOT NULL TO NULL
  "FirstName" text NULL,
  "LastName" text NULL,
  "Email" text NULL,
  "PhoneNumber" text NULL,
  "Role" integer NOT NULL,
  "CompanyId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."Users" ADD CONSTRAINT "PK_Users" PRIMARY KEY ("Id");

CREATE TABLE public."SkillSets" (
  "Id" SERIAL NOT NULL,
  "Name" text NOT NULL,
  "Shorthand" text NOT NULL,
  "Description" text NOT NULL, -- will have " " value
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."SkillSets" ADD CONSTRAINT "PK_SkillSets" PRIMARY KEY ("Id");

CREATE TABLE public."SeekerSkillSets" (
  "Id" SERIAL NOT NULL,
  "ProficiencyLevel" text NOT NULL, -- will have "1" value since the field no meaning
  "UserId" integer NOT NULL,
  "SkillDescription" text NOT NULL, -- Temporary value
  "SkillSetId" integer NULL, -- FROM NOT NULL TO NULL
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."SeekerSkillSets" ADD CONSTRAINT "PK_SeekerSkillSets" PRIMARY KEY ("Id");

CREATE TABLE public."Reviews" (
  "Id" SERIAL NOT NULL,
  "Rating" integer NULL, -- from NOT NULL to NULL
  "ReviewContent" text NULL, -- from NOT NULL to NULL
  "UserId" integer NULL,
  "CompanyId" integer NULL
);
ALTER TABLE public."Reviews" ADD CONSTRAINT "PK_Reviews" PRIMARY KEY ("Id");

CREATE TABLE public."JobTypes" (
  "Id" SERIAL NOT NULL,
  "Name" text NOT NULL,
  "Description" text NOT NULL
);
ALTER TABLE public."JobTypes" ADD CONSTRAINT "PK_JobTypes" PRIMARY KEY ("Id");

CREATE TABLE public."JobSkillSets" (
  "Id" SERIAL NOT NULL,
  "SkillSetId" integer NOT NULL, -- from NULL to NOT NULL
  "JobPostId" integer NOT NULL, -- from NULL to NOT NULL
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."JobSkillSets" ADD CONSTRAINT "PK_JobSkillSets" PRIMARY KEY ("Id");

CREATE TABLE public."JobPosts" (
  "Id" SERIAL NOT NULL,
  "JobTitle" text NOT NULL,
  "JobDescription" text NOT NULL,
  "Salary" text NOT NULL, -- from numeric to text
  "PostingDate" timestamp with time zone NOT NULL,
  "ExpiryDate" timestamp with time zone NOT NULL,
  "ExperienceRequired" text NOT NULL, -- from integer to text
  "QualificationRequired" text NULL,
  "ImageURL" text NULL,
  "SkillLevelRequired" integer NULL, -- from  NOT NULL to NULL
  "Benefits" text NULL,
  "IsActive" boolean NOT NULL,
  "UserId" integer NULL,
  "JobTypeId" integer NOT NULL, -- from NULL to NOT NULL
  "CompanyId" integer NOT NULL, -- from NULL to NOT NULL
  "JobLocationId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."JobPosts" ADD CONSTRAINT "PK_JobPosts" PRIMARY KEY ("Id");

CREATE TABLE public."JobPostActivitys" (
  "Id" SERIAL NOT NULL,
  "ApplicationDate" timestamp with time zone NOT NULL,
  "Status" integer NOT NULL,
  "UserId" integer NULL,
  "JobPostId" integer NULL,
  "CvId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."JobPostActivitys" ADD CONSTRAINT "PK_JobPostActivitys" PRIMARY KEY ("Id");

CREATE TABLE public."JobLocations" (
  "Id" SERIAL NOT NULL,
  "District" text NOT NULL,
  "City" text NOT NULL,
  "PostCode" text NOT NULL,
  "State" text NOT NULL,
  "Country" text NOT NULL,
  "StressAddress" text NOT NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."JobLocations" ADD CONSTRAINT "PK_JobLocations" PRIMARY KEY ("Id");


CREATE TABLE public."Position_Summary_Achievements" (
  "Id" SERIAL NOT NULL,
  "ApplyPosition" text NOT NULL, -- add 'Apply Position' to compare with JobPosts's JobTitle
  "Summary" text NOT NULL,
  "Achievements" text NULL, -- should be moved to 
  "UserId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."Position_Summary_Achievements" ADD CONSTRAINT "PK_Position_Summary_Achievements" PRIMARY KEY ("Id");

CREATE TABLE public."ExperienceDetails" (
  "Id" SERIAL NOT NULL,
  "CompanyName" text NOT NULL,
  "Position" text NOT NULL,
  "StartDate" timestamp with time zone NOT NULL,
  "EndDate" timestamp with time zone NOT NULL,
  "Responsibilities" text NOT NULL,
  "Achievements" text NULL, -- should be moved to 'Summary_Position_Achievements' table
  "UserId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."ExperienceDetails" ADD CONSTRAINT "PK_ExperienceDetails" PRIMARY KEY ("Id");

CREATE TABLE public."TempEducationDetails" (
  "Id" SERIAL NOT NULL,
  "Description" text NOT NULL,
  "UserId" integer NOT NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."TempEducationDetails" ADD CONSTRAINT "PK_TempEducationDetails" PRIMARY KEY ("Id");


CREATE TABLE public."EducationDetails" (
  "Id" SERIAL NOT NULL,
  "Name" text NOT NULL,
  "InstitutionName" text NOT NULL,
  "Degree" text NOT NULL,
  "FieldOfStudy" text NOT NULL,
  "StartDate" timestamp with time zone NOT NULL,
  "EndDate" timestamp with time zone NOT NULL,
  "GPA" numeric NOT NULL,
  "UserId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."EducationDetails" ADD CONSTRAINT "PK_EducationDetails" PRIMARY KEY ("Id");

CREATE TABLE public."Companys" (
  "Id" SERIAL NOT NULL,
  "CompanyName" text NOT NULL,
  "CompanyDescription" text NOT NULL,
  "WebsiteURL" text NOT NULL,
  "EstablishedYear" integer NOT NULL,
  "Country" text NOT NULL,
  "City" text NOT NULL,
  "Address" text NOT NULL,
  "NumberOfEmployees" integer NOT NULL,
  "BusinessStreamId" integer NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL,
  "ImageUrl" text NULL
);
ALTER TABLE public."Companys" ADD CONSTRAINT "PK_Companys" PRIMARY KEY ("Id");

CREATE TABLE public."CVs" (
  "Id" SERIAL NOT NULL,
  "Url" text NOT NULL,
  "UserId" integer NULL
);
ALTER TABLE public."CVs" ADD CONSTRAINT "PK_CVs" PRIMARY KEY ("Id");

CREATE TABLE public."BusinessStreams" (
  "Id" SERIAL NOT NULL,
  "BusinessStreamName" text NOT NULL,
  "Description" text NOT NULL,
  "CreatedDate" timestamp with time zone NULL,
  "ModifiedDate" timestamp with time zone NULL,
  "CreatedBy" uuid NULL,
  "ModifiedBy" uuid NULL,
  "IsDeleted" boolean NOT NULL
);
ALTER TABLE public."BusinessStreams" ADD CONSTRAINT "PK_BusinessStreams" PRIMARY KEY ("Id");

-- Define relation between tabels
ALTER TABLE "JobPosts" 
  ADD CONSTRAINT "fk_JobPost_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");
ALTER TABLE "JobPosts" 
  ADD CONSTRAINT "fk_JobPost_Company" FOREIGN KEY ("CompanyId") REFERENCES "Companys" ("Id");
ALTER TABLE "JobPosts" 
  ADD CONSTRAINT "fk_JobPost_JobType" FOREIGN KEY ("JobTypeId") REFERENCES "JobTypes" ("Id");
ALTER TABLE "JobPosts" 
  ADD CONSTRAINT "fk_JobPost_Location" FOREIGN KEY ("JobLocationId") REFERENCES "JobLocations" ("Id");

ALTER TABLE "JobSkillSets" 
  ADD CONSTRAINT "fk_JobSkillSet_JobPost" FOREIGN KEY ("JobPostId") REFERENCES "JobPosts" ("Id");
ALTER TABLE "JobSkillSets" 
  ADD CONSTRAINT "fk_JobSkillSet_SkillSet" FOREIGN KEY ("SkillSetId") REFERENCES "SkillSets" ("Id");

ALTER TABLE "SeekerSkillSets"
  ADD CONSTRAINT "fk_SeekerSkillSet_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

-- Should relax this constraints since skill of seeker not match with jobskillset's format
--ALTER TABLE "SeekerSkillSets" 
  --ADD CONSTRAINT "fk_SeekerSkillSet_SkillSet" FOREIGN KEY ("SkillSetId") REFERENCES "SkillSets" ("Id");

ALTER TABLE "Companys" 
  ADD CONSTRAINT "fk_Company_BusStream" FOREIGN KEY ("BusinessStreamId") REFERENCES "BusinessStreams" ("Id");

ALTER TABLE "JobPostActivitys"
  ADD CONSTRAINT "fk_JobPostActivitys_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");
ALTER TABLE "JobPostActivitys" 
  ADD CONSTRAINT "fk_JobPostActivitys_JobPost" FOREIGN KEY ("JobPostId") REFERENCES "JobPosts" ("Id");
ALTER TABLE "JobPostActivitys" 
  ADD CONSTRAINT "fk_JobPostActivitys_CV" FOREIGN KEY ("CvId") REFERENCES "CVs" ("Id");

ALTER TABLE "Reviews" 
  ADD CONSTRAINT "fk_Reviews_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");
ALTER TABLE "Reviews" 
  ADD CONSTRAINT "fk_Reviews_Company" FOREIGN KEY ("CompanyId") REFERENCES "Companys" ("Id");

-- add this foreign key for new table
ALTER TABLE "Position_Summary_Achievements" 
  ADD CONSTRAINT "FK_Position_Summary_Achievements_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

ALTER TABLE "ExperienceDetails" 
  ADD CONSTRAINT "FK_ExperienceDetail_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

ALTER TABLE "CVs" 
  ADD CONSTRAINT "fk_CV_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

ALTER TABLE "EducationDetails" 
  ADD CONSTRAINT "fk_EducationDetail_User" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

-- add a Temporaral table for demo
ALTER TABLE "TempEducationDetails" 
  ADD CONSTRAINT "fk_TempEducationDetails" FOREIGN KEY ("UserId") REFERENCES "Users" ("Id");

ALTER TABLE "Users" 
  ADD CONSTRAINT "fk_User_Company" FOREIGN KEY ("CompanyId") REFERENCES "Companys" ("Id");
