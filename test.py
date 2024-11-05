import openai
from config import settings
openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# List all files  
files = openai_client.files.list()  
print(files)
# Delete each file  
for file in files.data:  
    file_id = file.id
    openai_client.files.delete(file_id)  
    print(f"Deleted file: {file_id}")


vectors = openai_client.beta.vector_stores.list()
print(vectors)

for vector in vectors:  
    vector_id = vector.id
    openai_client.beta.vector_stores.delete(
        vector_store_id=vector_id
    )
    print(f"Deleted vector: {vector_id}")
