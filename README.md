# Example of vector databases produced via Large Language Model (LLM) embeddings
## Problem aiming to be solved

Websites, intranets, documents and other linked stores of information can have significant amount of trapped info that is hidden, unclear, or forgotten about.

Often, search engines built on top of these can be painfully finicky, with there being overly strong reliance on knowing just the correct terms to find the right information.

I am hoping to use semantic language embeddings produced using the llama2 large langauge model to turn a scraped website into something queryable with natural language.

## Solution approach

The intent here will be content matching, not a natural language response in full. That is, try to find the web-pages, and possibly paragraphs or sentences that seem most relevant to a natural language query.

As another options, I'd like to pre-define a number of queries and cache the best-matched results, I'd then use an LLM to try and align a natural language query best to the pre-defined ones we have from our corpus.

The intent with this is to also ideally set up an interface which is somewhat user friendly as a proof of concept but that also collects user ratings and both the query and response. This extra data then provides the 
avenue for reinforcement learning via human feedback.

The design of this app is try and split every thing into modules and allow full configuration of the package using a simple yaml setup document.

## Tool-stack
### Development
Testing framework: pytest
Logging framework: logging
Documentation: pdoc

### Package
llm interfaces: langchain
Vector database: chromadb
User interface: streamlit