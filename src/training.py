from sentence_transformers import SentenceTransformer
from typing import Literal

import torch.utils
from src.database import DB_Handling
import pandas as pd
import torch

class Database2Dataset(torch.utils.data.Dataset):
    """Dataset for SELECT query only"""
    def __init__(self, 
                 config_file_path:str, 
                 section: str, 
                 batch_size:int
                 )->None:

        self.db_handling = DB_Handling(config_file_path=config_file_path, 
                                  section= section)
        
    def __len__(self):
        """Must base on JobPostActivity with JobPostId and CVId"""
        



class Action_base(object):
    """
    Only Admin can have permission to use methods of this class
    """
    def __init__(self,
                 runing_mode: Literal["demo", "production"],
                 training_type: Literal["pretrained","fine_tuning"],
                 model_name: str = "all-MiniLM-L6-v2"
                 ) -> None:
        self.running_mode = runing_mode
        if training_type == "pretrained":
            self.model = SentenceTransformer(model_name)
        else:
            raise NotImplemented
        # create connection to DB

class Training_Model(Action_base):
    def __init__(self,
                 runing_mode: str,
                 training_type: str,
                 model_name: str
                 ) -> None:
        super().__init__(runing_mode, training_type, model_name)
        
    def _prepare_dataset(self):
        pass
        
    def start_training(self):
        pass

class Compute_Assign_Score(Action_base):
    def __init__(self,
                 runing_mode: str,
                 training_type: str,
                 model_name: str
                 ) -> None:
        super().__init__(runing_mode, training_type, model_name)
    
    def _prepare_dataset(self, data_path:str = None):
        if self.running_mode == "demo":
            assert data_path is not None, "Demo purpose required external data source"
            engine = DB_Handling()
            # create tables
            engine.create_tables(table_name_list= ["resume","jobpost","score"])

            ##### Resume data #####
            demo_data = pd.read_csv("demo_data\livecareer_resume_dataset\Resume\Resume.csv")
            filter_data = demo_data["Resume_str"]
            results = [filter_data.iat[row_id]
                    for row_id in range(len(filter_data))]

            # cleaning for correct format
            results = [(" ".join([ele.lower().replace("\n","")
                                    for ele in content.split(" ") 
                                    if ele != ""
                                    ]))
                    for content in results]
            engine.insert(target_table= "resume", insertion_data= results)


        else:
            raise NotImplemented

    def compute_and_assign_score(self):
        # Two lists of sentences
        sentences1 = [
            "The new movie is awesome",
            "The cat sits outside",
            "A man is playing guitar",
        ]

        sentences2 = [
            "The dog plays in the garden",
            "The new movie is so great",
            "A woman watches TV",
        ]

        # Compute embeddings for both lists
        embeddings1 = self.model.encode(sentences1)
        embeddings2 = self.model.encode(sentences2)

        # Compute cosine similarities
        similarities = self.model.similarity(embeddings1, embeddings2)

        # Output the pairs with their score
        for idx_i, sentence1 in enumerate(sentences1):
            print(sentence1)
            for idx_j, sentence2 in enumerate(sentences2):
                print(f" - {sentence2: <30}: {similarities[idx_i][idx_j]:.4f}")
