#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import YoutubeLoader


# In[2]:


loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=g3G--ff5_4E", add_video_info=True)


# In[3]:


result = loader.load()


# In[4]:


print (type(result))
print (f"Found video from {result[0].metadata['author']} that is {result[0].metadata['length']} seconds long")
print ("")
print (result)


# In[5]:


OPENAI_API_KEY = ''
#Result is txt file after transcription module
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
#Normal summarization for short podcasts
chain = load_summarize_chain(llm, chain_type="stuff", verbose=False)


# In[6]:


# txt_path = 'podcastexample2.txt'
# with open(txt_path, 'r') as f:
#   result = f.read()


# In[7]:


# result2 = list([Document(page_content='LADIES AND GENTLEMEN, PEDRO PASCAL! [ CHEERS AND APPLAUSE ] >> THANK YOU, THANK YOU. THANK YOU VERY MUCH. I\'M SO EXCITED TO BE HERE. THANK YOU. I SPENT THE LAST YEAR SHOOTING A SHOW CALLED "THE LAST OF US" ON HBO. FOR SOME HBO SHOES, YOU GET TO SHOOT IN A FIVE STAR ITALIAN RESORT SURROUNDED BY BEAUTIFUL PEOPLE, BUT I SAID, NO, THAT\'S TOO EASY. I WANT TO SHOOT IN A FREEZING CANADIAN FOREST WHILE BEING CHASED AROUND BY A GUY WHOSE HEAD LOOKS LIKE A GENITAL WART. IT IS AN HONOR BEING A PART OF THESE HUGE FRANCHISEs LIKE "GAME OF THRONES" AND "STAR WARS," BUT I\'M STILL GETTING USED TO PEOPLE RECOGNIZING ME. THE OTHER DAY, A GUY STOPPED ME ON THE STREET AND SAYS, MY SON LOVES "THE MANDALORIAN" AND THE NEXT THING I KNOW, I\'M FACE TIMING WITH A 6-YEAR-OLD WHO HAS NO IDEA WHO I AM BECAUSE MY CHARACTER WEARS A MASK THE ENTIRE SHOW. THE GUY IS LIKE, DO THE MANDO VOICE, BUT IT\'S LIKE A BEDROOM VOICE. WITHOUT THE MASK, IT JUST SOUNDS PORNY. PEOPLE WALKING BY ON THE STREET SEE ME WHISPERING TO A 6-YEAR-OLD KID. I CAN BRING YOU IN WARM, OR I CAN BRING YOU IN COLD. EVEN THOUGH I CAME TO THE U.S. WHEN I WAS LITTLE, I WAS BORN IN CHILE, AND I HAVE 34 FIRST COUSINS WHO ARE STILL THERE. THEY\'RE VERY PROUD OF ME. I KNOW THEY\'RE PROUD BECAUSE THEY GIVE MY PHONE NUMBER TO EVERY PERSON THEY MEET, WHICH MEANS EVERY DAY, SOMEONE IN SANTIAGO WILL TEXT ME STUFF LIKE, CAN YOU COME TO MY WEDDING, OR CAN YOU SING MY PRIEST HAPPY BIRTHDAY, OR IS BABY YODA MEAN IN REAL LIFE. SO I HAVE TO BE LIKE NO, NO, AND HIS NAME IS GROGU. BUT MY COUSINS WEREN\'T ALWAYS SO PROUD. EARLY IN MY CAREER, I PLAYED SMALL PARTS IN EVERY CRIME SHOW. I EVEN PLAYED TWO DIFFERENT CHARACTERS ON "LAW AND ORDER." TITO CABASSA WHO LOOKED LIKE THIS. AND ONE YEAR LATER, I PLAYED REGGIE LUCKMAN WHO LOOKS LIKE THIS. AND THAT, MY FRIENDS, IS CALLED RANGE. BUT IT IS AMAZING TO BE HERE, LIKE I SAID. I WAS BORN IN CHILE, AND NINE MONTHS LATER, MY PARENTS FLED AND BROUGHT ME AND MY SISTER TO THE U.S. THEY WERE SO BRAVE, AND WITHOUT THEM, I WOULDN\'T BE HERE IN THIS WONDERFUL COUNTRY, AND I CERTAINLY WOULDN\'T BE STANDING HERE WITH YOU ALL TONIGHT. SO TO ALL MY FAMILY WATCHING IN CHILE, I WANT TO SAY [ SPEAKING NON-ENGLISH ] WHICH MEANS, I LOVE YOU, I MISS YOU, AND STOP GIVING OUT MY PHONE NUMBER. WE\'VE GOT AN AMAZING SHOW FOR YOU TONIGHT. COLDPLAY IS HERE, SO STICK', lookup_str='', metadata={'source': 'QsYGlZkevEg', 'title': 'Pedro Pascal Monologue - SNL', 'description': 'First-time host Pedro Pascal talks about filming The Last of Us and being recognized by fans.\n\nSaturday Night Live. Stream now on Peacock: https://pck.tv/3uQxh4q\n\nSubscribe to SNL: https://goo.gl/tUsXwM\nStream Current Full Episodes: http://www.nbc.com/saturday-night-live\n\nWATCH PAST SNL SEASONS\nGoogle Play - http://bit.ly/SNLGooglePlay\niTunes - http://bit.ly/SNLiTunes\n\nSNL ON SOCIAL\nSNL Instagram: http://instagram.com/nbcsnl\nSNL Facebook: https://www.facebook.com/snl\nSNL Twitter: https://twitter.com/nbcsnl\nSNL TikTok: https://www.tiktok.com/@nbcsnl\n\nGET MORE NBC\nLike NBC: http://Facebook.com/NBC\nFollow NBC: http://Twitter.com/NBC\nNBC Tumblr: http://NBCtv.tumblr.com/\nYouTube: http://www.youtube.com/nbc\nNBC Instagram: http://instagram.com/nbc\n\n#SNL #PedroPascal #SNL48 #Coldplay', 'view_count': 1433225, 'thumbnail_url': 'https://i.ytimg.com/vi/QsYGlZkevEg/sddefault.jpg', 'publish_date': datetime.datetime(2023, 2, 4, 0, 0), 'length': 224, 'author': 'Saturday Night Live'}, lookup_index=0)])


# In[8]:


chain.run(result)


# In[50]:


## Long Videos


# In[51]:


loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=5p248yoa3oE", add_video_info=True)


# In[52]:


result = loader.load()


# In[53]:


text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
texts = text_splitter.split_documents(result)


# In[55]:


texts


# In[56]:


chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
chain.run(texts[:4])


# In[ ]:




