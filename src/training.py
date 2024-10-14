from sentence_transformers import SentenceTransformer
from typing import Literal, Dict, List, Union
from tqdm import tqdm
import torch.utils
from src.database import Query2MainDB
import torch

class Database2Dataset(torch.utils.data.Dataset):
    """Dataset/Dataloader for SELECT query only"""
    def __init__(self, 
                 config_file_path:str, 
                 section: str,
                 )->None:
        
        self.db_handling = Query2MainDB(config_file_path=config_file_path, 
                                  section= section)
        self.id_pairs = self.db_handling.get_available_activity()
        assert isinstance(self.id_pairs,list), "Cannot query to DB, JobPostActivity table"

    def __len__(self):
        """Must base on JobPostActivity with JobPostId and UserId"""
        return len(self.id_pairs)

    def __getitem__(self, index:int)->tuple[int,str]:
        current_ids = self.id_pairs[index]

        query_data = self.db_handling.query(jobpost_id= current_ids['JobPostId'],
                                            user_id=current_ids['UserId'])

        return (current_ids['Id'],
                query_data['resume'],
                query_data['jobpost']
            )

class Action_base(object):
    """
    Only Admin can have permission to use methods of this class
    """
    def __init__(self,
                 runing_mode: Literal["demo", "production"],
                 model_type: Literal["pretrained","fine_tuning"],
                 model_name: str = "all-MiniLM-L6-v2"
                 ) -> None:
        self.running_mode = runing_mode
        if model_type == "pretrained":
            self.model = SentenceTransformer(model_name)
        else:
            raise NotImplemented

# class Fine_tuning(Action_base):
#     def __init__(self, runing_mode: Literal['demo'] | Literal['production'], model_type: Literal['pretrained'] | Literal['fine_tuning'], model_name: str = "all-MiniLM-L6-v2") -> None:
#         super().__init__(runing_mode, model_type, model_name)




class Compute_Assign_Score(Action_base):
    """Compute Consine similarity score 
    between a jobpost and user's resume
    similarity socre range from 0 to 1
    near 1 indicates high similarity
    near 0 indicates very low similarity
    """
    def __init__(self,
                 runing_mode: str,
                 model_type: str,
                 model_name: str,
                 db_config_file_path:str,
                 section: str,
                 batch_size:int,
                 ) -> None:
        super().__init__(runing_mode, model_type, model_name)

        dataset = Database2Dataset(db_config_file_path, section)
        self.loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, drop_last = False)
        self.batch_size = batch_size
        self.db_config_file_path = db_config_file_path
        self.section = section

    def compute_and_assign_score(self):
        score_output: List[Dict[str,Union[int,float]]] = []

        for batchId, batch_resume, batch_jobpost in tqdm(self.loader, total= len(self.loader)):
            # Compute embeddings for both lists
            
            resume_embeddings = self.model.encode(batch_resume)
            jobpost_embeddings = self.model.encode(batch_jobpost)
            
            # Compute cosine similarities
            similarities = self.model.similarity(resume_embeddings, jobpost_embeddings)
            assert similarities.shape[0] == batchId.shape[0] \
                    and similarities.shape[1] == batchId.shape[0], f"Found\
                {similarities.shape} vs {batchId.shape}"
            
            batch_score= [{'Id':batchId[idx].item(),
                            'Score': similarities[idx][idx].item()
                        } 
                        for idx in range(batchId.shape[0])
                        ]

            score_output.extend(batch_score)
        
        # update score
        db_handling = Query2MainDB(config_file_path=self.db_config_file_path, 
                                  section= self.section)
        status = db_handling.update_score2table(update_data= score_output)
        if status:
            print("Done")
        else:
            print("False to assign score")
