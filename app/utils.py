import pandas as pd
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Question(BaseModel):
    text: str
    category_options: List[int]  # Changed to List[int]
    correct_category: int  # Changed to int
    correct_value: int

def validate_csv(df):
    logger.debug(f"Validating DataFrame: {df}")
    
    if df.empty:
        logger.debug("DataFrame is empty")
        return False
    
    if len(df.columns) != 3:
        logger.debug(f"DataFrame has {len(df.columns)} columns, expected 3")
        return False
    
    try:
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1])
        df.iloc[:, 2] = pd.to_numeric(df.iloc[:, 2])
        logger.debug("DataFrame validation successful")
        return True
    except Exception as e:
        logger.debug(f"DataFrame validation failed: {str(e)}")
        return False

def parse_csv(df):
    logger.debug(f"Parsing DataFrame: {df}")
    questions = []
    
    # Get unique values from second column for category options, convert to int, and sort
    category_options = sorted(df.iloc[:, 1].unique().astype(int).tolist())
    
    for index, row in df.iterrows():
        if pd.isna(row.iloc[0]):
            logger.debug(f"Empty row found at index {index}, stopping parsing")
            break
            
        try:
            question = Question(
                text=str(row.iloc[0]),
                category_options=category_options,
                correct_category=int(row.iloc[1]),
                correct_value=int(row.iloc[2])
            )
            questions.append(question.dict())
            logger.debug(f"Question added: {question}")
        except (ValidationError, ValueError) as e:
            logger.debug(f"Error parsing row {index}: {str(e)}")
            continue

    logger.debug(f"Total questions parsed: {len(questions)}")
    return questions

