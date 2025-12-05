from fastapi import Depends
from fastapi import Body

from mategen.mategen_class import MateGenClass
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from openai import OpenAI


def get_mate_gen(
        # user_id: str = Body(None, description="Unique user identifier"),
        thread_id: str = Body(None, description="conversation id"),
        enhanced_mode: bool = Body(False, description="Enable enhanced mode"),
        knowledge_base_chat: bool = Body(False, description="Enable knowledge base chat"),
        knowledge_base_name_id: str = Body(None, description="id of the knowledge_base_chat is enabled"),
        db_name_id: str = Body(None, description="Database name"),
) -> MateGenClass:
    """
    Used to generate an instance of the mategen Class
    :param api_key:
    :param enhanced_mode:
    :param knowledge_base_chat:
    :param kaggle_competition_guidance:
    :param competition_name:
    :param knowledge_base_name:
    :return:
    """
    return MateGenClass(thread_id, enhanced_mode, knowledge_base_chat, knowledge_base_name_id, db_name_id)




