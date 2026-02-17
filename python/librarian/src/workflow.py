from agno.workflow import Step, Workflow

from reader import sample_file
from agent_librarian import agent
from send_to_shelf import send_to_shelf


# STEPS
step_1 = Step(
    name='Sample file',
    description='Extract a sample of the document content to help the agent understand the document.',
    executor=sample_file
)

step_2 = Step(
    name='Librarian analysis',
    description='Analyze the document and generate a filename, path (shelf), summary and tags.',
    agent=agent
)

step_3 = Step(
    name='Send to shelf',
    description='Send the analyzed file to the appropriate folder (shelf).',
    executor=send_to_shelf
)

# WORKFLOW
workflow = Workflow(
    name='Librarian execution pipeline',
    steps=[
        step_1,
        step_2,
        step_3
    ],
    
    debug_mode=True
)