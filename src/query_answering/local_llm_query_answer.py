from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from transformers import AutoTokenizer, pipeline
import torch
from langchain.embeddings import HuggingFaceInstructEmbeddings


# Hugging face local example in collab notebook
# https://colab.research.google.com/drive/12v2ZBIucDZ-MBTX4VGEMJR4Fxf-EOYN0#scrollTo=JCb7algHVxeI
# https://discuss.huggingface.co/t/using-hugging-face-models-with-private-company-data/56403
# Parameters
model_name_used = "tiiuae/falcon-7b-instruct"
path_to_model_on_disk = r"F:\reference_models\large_language_models\llama2\falcon-7b-instruct"

# Load up the local llm and 
llama2_model_tokeniser = AutoTokenizer.from_pretrained(path_to_model_on_disk)

llama2_model_pipeline = pipeline(
    "text-generation",
    model = path_to_model_on_disk,
    tokenizer = llama2_model_tokeniser,
    torch_dtype = torch.bfloat16,
    trust_remote_code = False,
    device_map = "cpu", # -1 should map to CPU "auto",
    max_length = 200,
    do_sample = True,
    top_k = 10,
    num_return_sequences = 1,
    eos_token_id = llama2_model_tokeniser.eos_token_id,
    pad_token_id = llama2_model_tokeniser.eos_token_id,
)

llama2_instruct_7b_llm = HuggingFacePipeline(pipeline = llama2_model_pipeline)

# Once model pipeline setup, use it for example
template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=llama2_instruct_7b_llm)

questions = [
    "Who proved the Efficient Market Hypothesis?",
    "Who disproved the Efficient Market Hypothesis?",
    "Who proved the Poincaré conjecture for n >= 5?",  # Stephen Smale
    "Who proved the Poincaré conjecture for n = 4?",  # Michael Freedman
    "Who proved the Poincaré conjecture for n = 3?",  # Grigori Perelman
    "Is the sum of all natural numbers equal to -1/12?",
]

for question in questions:
    result = llm_chain.run(question)
    print(question)
    print(result)

# Took about 10 minutes to 20 minutes
# Who proved the Efficient Market Hypothesis?
# The Efficient Market Hypothesis is a widely accepted theory in finance that states that market prices always react to all publicly available information. This hypothesis was put to test by a group of academics, and the most famous experiment was carried out by the University of Pennsylvania. The results of the experiment found that the stock prices in the experiment followed random, rather than efficient, patterns. These findings were later reinforced by a study of stock prices in New York over a period of 40 years. This evidence led to the conclusion that market prices are often affected by random movements in the wider economy that are beyond market players' control.