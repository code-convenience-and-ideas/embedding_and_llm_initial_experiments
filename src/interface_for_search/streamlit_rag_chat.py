import streamlit as st
from collections import defaultdict
from streamlit_star_rating import st_star_rating
# from streamlit_javascript import st_javascript
from glob import glob
import os
from pathlib import Path
import base64
import mimetypes

# Add markdown as a mimetype before use
mimetypes.add_type('text/plain', '.md')

# Set up the prompt templates
empty_prompt_name = "empty"
empty_prompt_text = ""

prompt_templates = defaultdict(lambda: "", **{
    empty_prompt_name: empty_prompt_text,
    "summary_of_reports": "Which providers have been asked to write a medical report for us? Please list them all.",
    "summarise_diagnoses": "Please identify and list all of the medical diagnoses for the claim.",
    "summarise_treatment": "Please summarise and list the treatment that has occurred on the claim.",
    "referral_search": "What medical referrals have occurred to other providers?",
    "mental_health_search": "Has there been any mentions of mental health issues for the claimant?"
})

# Setup the title + page config
# Start with file upload option
llm_rag_example_page_title = "📝 File Search And Answer with RAG"
st.set_page_config(page_title = llm_rag_example_page_title)
st.title(llm_rag_example_page_title)

# Set up some parameters 
# Note context window is in tokens, not characters
# but this is arbitrary for my convenience
llm_max_context_window = 4096

# Set up some session state to use for storing values and some responsiveness
if 'prompt_option' not in st.session_state:
    # By default, we will use an empty prompt
    st.session_state.prompt_option = empty_prompt_name

if 'prompt_template' not in st.session_state:
    # By default, we will use an empty tempalte
    st.session_state.prompt_template = prompt_templates[st.session_state.prompt_option]

if 'response_rating' not in st.session_state:
    # Default to no value for quality rating of response
    st.session_state.response_rating = None

if 'query_history' not in st.session_state:
    # Default to empty dictionary
    st.session_state.query_history = dict()



def update_prompt_template(button_key: str):
    st.session_state.prompt_option = button_key
    st.session_state.prompt_template = prompt_templates[button_key]

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[Feedback on app overall]()"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Setup up the section where the use inputs their query
st.write("## Query")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

# Add a dropdown list of prompt templates
## Options for prompt templates - select dropdown menu
prompt_template_buttons = [
    {"label": "Report Summary",
     "value": "summary_of_reports"},
    {"label": "Diagnosis Query",
     "value": "summarise_diagnoses"},
    {"label": "Treatment Query",
     "value": "summarise_treatment"},
    {"label": "Find referrals",
     "value": "referral_search"},
    {"label": "Mental Health mentions",
     "value": "mental_health_search"}
]

prompt_label_to_keys = defaultdict(lambda: None,
                                   {
                                       entry['label']: entry['value']
                                       for entry in prompt_template_buttons
                                })

prompt_template_labels = list(prompt_label_to_keys.keys())

## add the select box and update session state on update
def on_prompt_template_selection():
    return("")

prompt_selected = st.selectbox(
    "If desired, please select a prompt template.",
    options = prompt_template_labels,
    index = None,
    placeholder = "Default is no template."
)

prompt_template_key = prompt_label_to_keys[prompt_selected]

## If option select, then change session state
if prompt_template_key is not None:
    st.session_state.prompt_option = prompt_template_key
    st.session_state.prompt_template = prompt_templates[prompt_template_key]
    st.write('You selected:', prompt_template_key)

## Add a clear button as well - on click it defaults session state to null template
def clear_query_on_click():
    st.session_state.prompt_option = empty_prompt_name
    st.session_state.prompt_template = prompt_templates[empty_prompt_name]

cleared_template = st.button(
    label = "Clear prompt.",
    key = "clear_prompt",
    on_click = clear_query_on_click
)

if cleared_template:
    st.session_state.prompt_option = empty_prompt_name
    st.session_state.prompt_template = prompt_templates[empty_prompt_name]

# Use the chosen template and allow user to edit
question = st.text_area(
    label = "Ask information about the claim",
    value = st.session_state.prompt_template,
    max_chars = llm_max_context_window,
)

# Ask the user to rate their answer
def process_rating_click(rating_value):
    st.write(f"Response rated as: **{rating_value}** out of 5 starts")

stars = st_star_rating("Please rate the response the model gave",
                       maxValue = 5,
                       defaultValue = 3,
                       key = "response_rating",
                       on_click = process_rating_click)

# if user submits the file then give a response
st.write("## Answer")

# Aim to set up example where document viewer is used to preview identified docs
n_docs_to_show = stars

# Dummy example is the hash of question
st.write(f"You asked: {question} of me."
         f"I currently cannot response intelligently.")

st.write(f"### Model sources for answer.")

path_to_documents = r"C:\Users\Alex\Google Drive\projects\llama2_retrieval_augmented_generation\data"
source_documents = glob(os.path.join(path_to_documents, 'moby_dick*'))
document_basenames = [os.path.basename(document_path) for document_path in source_documents]

# Add document view expanders with embeds / iframes to show the different document types
default_doc_height = 400
default_doc_width = 800
# pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

displayable_mime_types = {
    "application/pdf",
    "text/plain",
    "text/html",
}

document_columns = st.columns([1], gap="small")

for doc_index in range(0, n_docs_to_show):
    # Use the file names and the like to decode the file information
    doc_name = document_basenames[doc_index]
    doc_path = Path(source_documents[doc_index])
    doc_type = os.path.splitext(doc_name)[1]
    doc_mimetype = mimetypes.guess_type(doc_name)[0]

    # Set up the expander with titel and basic format
    doc_expander = document_columns[0].expander(f"{doc_name}")
    doc_expander.write(f"This is a test for showing {doc_name} dynamically.")
    doc_expander.write(f"{doc_mimetype} for {doc_name}")

    if doc_mimetype in displayable_mime_types:
        # Load in the relevant file and use embed to try and display it
        with open(Path(source_documents[doc_index]), "rb") as source_file_from_rag:
            base64_file = base64.b64encode(source_file_from_rag.read()).decode('utf-8')
            print("Loaded file from disk again")

        # Create the display iframe
        # embed_doc_display = f'<iframe src="data:{doc_mimetype};base64,{base64_file}" width="{default_doc_width}" height="{default_doc_height}" type="{doc_mimetype}"></iframe>'
        embed_doc_display = f'<embed src="data:{doc_mimetype};base64,{base64_file}" width="100%" height="{default_doc_height}" type="{doc_mimetype}"></embed>'

        # Now display it in the expander
        doc_expander.markdown(embed_doc_display, unsafe_allow_html=True)
    else:
        doc_expander.write(f"Sorry! Can't show {doc_type} files in the browser.")

    # doc_expander.write()
