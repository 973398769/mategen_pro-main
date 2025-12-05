from fastapi import FastAPI, Request, HTTPException, Depends, Body
import os
from mategen.mategen_class import MateGenClass
from init_interface import get_mate_gen
from pathlib import Path
import json

from pytanic_router import ChatRequest


def initialize_mate_gen(mate_gen: MateGenClass = Depends(get_mate_gen)):
    """
    Initialize MetaGen instance
    :param mate_gen:
    :return:
    """
    try:
        global global_instance
        global_instance = mate_gen
        # Return corresponding information based on initialization result
        return {"status": 200, "data": "mategen instance initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def custom_chat(request: ChatRequest):
    try:
        response = global_instance.chat(request.question)
        return {"status": 200, "data": response['data']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_knowledge_bases():
    # Get KNOWLEDGE_LIBRARY_PATH environment variable
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        return {"error": f"{main_json_file} does not exist. Please create the knowledge base first."}

    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)

    return list(main_mapping.keys())
