from agno.workflow import StepInput, StepOutput


def send_to_shelf(step_input: StepInput) -> StepOutput:
    
    src = step_input.input['file_path']
    library_path = step_input.input['library_path']

    agent_librarian_output = step_input.previous_step_content

    dst = library_path / agent_librarian_output.file_path
    
    try:
        dst.mkdir(parents=True, exist_ok=True)
        src.rename(dst / agent_librarian_output.file_name)    
    except Exception:
        return StepOutput(content='', success=False)
    else:
        return StepOutput(content='', success=True)