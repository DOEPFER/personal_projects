from pypdf import PdfReader

from agno.workflow import StepInput, StepOutput


def sample_file(step_input: StepInput) -> StepOutput:

    library_shelves = step_input.input['library_shelves']
    file_path = step_input.input['file_path']
    
    max_pages = 15

    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)

            metadata = pdf.metadata        
            metadata = {
                'title': metadata.title if metadata.title is not None else '',
                'author': metadata.author if metadata.author is not None else '',
                'subject': metadata.subject if metadata.subject is not None else ''
            }

            # metadata_xmp = pdf.xmp_metadata
            # metadata_xmp = {
            #     'title': metadata_xmp.dc_title if metadata_xmp.dc_title is not None else '',
            #     'author': metadata_xmp.dc_creator if metadata_xmp.dc_creator is not None else '',
            #     'subject': metadata_xmp.dc_description if metadata_xmp.dc_description is not None else ''
            # }
            
            total_pages = len(pdf.pages)

            max_pages = min(max_pages, total_pages)

            sample = ''
            for i in range(max_pages):
                page = pdf.pages[i]
                sample += page.extract_text()
    except Exception:
        return StepOutput(content='', success=False)
    else:
        return StepOutput(content={'metadata': metadata, 'sample': sample, 'library_shelves': library_shelves}, success=True)