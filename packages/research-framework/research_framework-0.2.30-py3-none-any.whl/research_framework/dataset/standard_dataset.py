from torch.utils.data import Dataset
import pandas as pd
import scipy
from typing import Any, Optional, Type
import numpy as np

class StandardDataset(Dataset):
    def __init__(self, df:Optional[pd.DataFrame|Type[callable]], vectors:Any):
        self.df = df
        self.vectors = vectors
        if scipy.sparse.issparse(self.vectors):
            self.vectors = self.vectors.astype(float).tocsr()

    def __len__(self):
        if callable(self.df):
            self.df = self.df()
            
        return len(self.df.index)
    
    def __getitem__(self, index) -> Any:
        if callable(self.df):
            self.df = self.df()
            
        if scipy.sparse.issparse(self.vectors):
            if hasattr(index, "__len__"):
                return self.df.iloc[index], self.vectors[index, :]
            else:
                return self.df.iloc[index], self.vectors.getrow(index)
        else:
            if type(self.vectors) is list:
                self.vectors = np.array(self.vectors)
            return self.df.iloc[index], self.vectors[index]
            