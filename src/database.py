from configparser import ConfigParser
from typing import Dict, Literal, List, Tuple, Union
import psycopg2

class DB_Handling(object):
    def __init__(self) -> None:
        self.config = self._get_DB_config()

    def _get_DB_config(self, file_path = "src/db.ini", section = "postgresql")->Dict:
        parser = ConfigParser()
        parser.read(file_path)
        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, file_path))
        return config

    def _get_cursor_and_connection(self):
        try:
        # connecting to the PostgreSQL server
            conn = psycopg2.connect(**self.config)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

        cur = conn.cursor()

        return conn, cur

    # create tables
    def create_table(self, table_name_list: List[Literal["resume", "jobpost","score"]])->None:
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
