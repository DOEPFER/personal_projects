import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat

from agent_librarian_io import LibrarianInput, LibrarianOutput
from prompts import DESCRIPTION, INSTRUCTIONS


load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

agent = Agent(
    name='Librarian',
    role='Librarian',

    model=OpenAIChat(id='gpt-4o-mini', api_key=OPENAI_API_KEY),

    description=DESCRIPTION,
    instructions=INSTRUCTIONS,

    input_schema=LibrarianInput,
    output_schema=LibrarianOutput,
    
    debug_mode=True
)