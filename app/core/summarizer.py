import os
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import YoutubeLoader
from app.utils.redis_consts import set_summary_status, is_summarization_running

async def summarize_text(file_id):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    #Result is txt file after transcription module
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_summarize_chain(llm, chain_type="stuff", verbose=False)

    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    transcript_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "transcripts", f"{file_id}.txt"))
    summary_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "summary", f"{file_id}.txt"))

    set_summary_status("True")
    with open(transcript_file, 'r',encoding="utf8") as f:
        result = f.read()
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "],chunk_size=200, chunk_overlap=50)
    transcript_subsection_characters = 2325
    docs = text_splitter.create_documents([result[:transcript_subsection_characters]])
    print (f"You have {len(docs)} docs. First doc is {llm.get_num_tokens(docs[0].page_content)} tokens")
    
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)
    print(chain.run(docs))

    with open(summary_file, "a") as tfile:
        tfile.write(chain.run(docs) + "\n")
        set_summary_status("False")
    
    while is_summarization_running():
        time.sleep(.5)