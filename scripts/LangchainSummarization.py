from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import YoutubeLoader


OPENAI_API_KEY = ''
#Result is txt file after transcription module
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

chain = load_summarize_chain(llm, chain_type="stuff", verbose=False)

txt_path = 'lifeAdvice.txt'
with open(txt_path, 'r',encoding="utf8") as f:
   result = f.read()

text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "],chunk_size=200, chunk_overlap=50)

transcript_subsection_characters = 2325
docs = text_splitter.create_documents([result[:transcript_subsection_characters]])
print (f"You have {len(docs)} docs. First doc is {llm.get_num_tokens(docs[0].page_content)} tokens")

chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)
print(chain.run(docs))