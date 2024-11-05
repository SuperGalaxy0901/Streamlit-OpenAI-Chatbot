from config import settings
from langfuse import Langfuse 
from langfuse.openai import openai  
from langfuse.decorators import langfuse_context, observe
import hashlib
import secrets
import io
import time
from database.chat_manager import create_chat, get_user_chats
from database.cost_manager import insert_cost

openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# Initialize Langfuse Client  
langfuse_client = Langfuse(  
    secret_key=settings.LANGFUSE_SECRET_KEY,  
    public_key=settings.LANGFUSE_PUBLIC_KEY,  
    host=settings.LANGFUSE_HOST
)

@observe()
def generate_vector_store(uploaded_files, user_id):
    # Generate Vector Name Using Hash
    random_bytes = secrets.token_bytes(64)
    hash_object = hashlib.sha256()
    hash_object.update(random_bytes)
    vector_name = hash_object.hexdigest()

    # Init File for upload OpenAI
    file_content = uploaded_files[0].getvalue()
    file_bytes_io = io.BytesIO(file_content.encode('utf-8') if isinstance(file_content, str) else file_content)
    file_bytes_io.name = uploaded_files[0].name

    # Upload File on OpenAI store
    file = openai_client.files.create(
        file=file_bytes_io,
        purpose='assistants'
    )
    uploaded_files[0] = file.id

    # Vector Store
    vector = openai_client.beta.vector_stores.create(
        name=vector_name
    )
    openai_client.beta.vector_stores.files.create(
        vector_store_id=vector.id,
        file_id=file.id
    )

    # chat assistant
    assistant = openai_client.beta.assistants.create(
        instructions="Use the file provided as your knowledge base to best respond to customer queries. Only include at least on file citation(for example: 【4:1†source】) in the answer.",
        model="gpt-4o-mini",
        tools=[
            { 
                "type": "file_search",
            }
            ],
        tool_resources={
            "file_search": {
            "vector_store_ids":[vector.id]
            }
        }
    )

    # chat thread
    thread = openai_client.beta.threads.create()
    create_chat(user_id, vector.id, thread.id, file.id, assistant.id)
    print(f"Thread: {thread.id}")
    print(f"Assistant: {assistant.id}")
    return thread.id, assistant.id, file_bytes_io.name

@observe()
def get_conversational_chain(user_question, thread_id, assistant_id, file_name, session_id):
    """Ignore thread_id parameter due to cost limit"""
    print(f"Thread: {thread_id}")
    print(f"Assistant: {assistant_id}")
    print(f"User Question: {user_question}")
    if user_question == "":
        return
    thread = openai_client.beta.threads.create()
    openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_question + """Include references after the answer in this format: 
            <div class="file-citation">
                <h3 class="citation-title">File Name with extension Here</h3>
                > Exact contents of the references(10 sentences)
            </div>

            Never produce unnecessary statements like "For more details, here is the citation formatted as requested:"
            Only include at least on file citation(for example: 【4:1†source】) in the answer and do not include file citations(for example: 【4:1†source】) in the references.
            Generate answer at any cost.
            """
    )
    with openai_client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant_id,
    instructions=f"You will act as a helpful assistant. Please analyze {file_name} and provide accurate answers to user question. Only include at least on file citation(for example: 【4:1†source】) in the answer.",
    ) as stream:
        for event in stream:  

            if event.event == 'thread.run.step.created':  
                print('\nMessage creation detected...')  

                for text in stream.text_deltas:  
                    yield text
            elif event.event == 'thread.message.delta':  
                yield event.data.delta.content[0].text.value  

    if stream._current_message_content:
        file_citation_annotations = stream._current_message_content.text.annotations
        yield file_citation_annotations

    # log internal generation within the openai assistant as a separate child generation to langfuse  
    if stream.current_run:  
        # langfuse_client.generation(  
        #     trace_id=langfuse_context.get_current_trace_id(),  
        #     parent_observation_id=langfuse_context.get_current_observation_id(),  
        #     model=stream.current_run.model,
        #     usage=stream.current_run.usage,  
        #     input=user_question,  
        #     output=[r['text'].value for r in stream.current_run.events if r['event'] == 'thread.message.delta']  
        # )
        
        # Extract and print cost data
        cost_data = cost_for_tokens(stream.current_run.usage)
        print(f"Cost for this response: {cost_data}")
        insert_cost(session_id, cost_data)

@observe()
def generate_questions(thread_id, assistant_id, file_name, session_id):
    thread = openai_client.beta.threads.create()
    openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Generate 3 questions for the {file_name}. Only output 3 questions and never output statement."
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=f"You will act as a helpful assistant. Please analyze {file_name} and provide accurate answers to user question."
    )

    retrieved_run = openai_client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    counter = 0
    while retrieved_run.status != "completed":
        retrieved_run = openai_client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        counter += 1
        if counter % 10 == 0:
            time.sleep(1)
    
    thread_messages = openai_client.beta.threads.messages.list(thread.id)
    
    # log the generation for tracking cost  
    if retrieved_run:  
        langfuse_client.generation(  
            trace_id=langfuse_context.get_current_trace_id(),  
            parent_observation_id=langfuse_context.get_current_observation_id(),  
            model=retrieved_run.model,  
            usage=retrieved_run.usage,  
            input=f"generate 3 questions for the {file_name}. only output 3 questions",  
            output=[msg.content[0].text.value for msg in thread_messages.data if msg.role == 'assistant']  
        )
        # Extract and print cost data
        cost_data = cost_for_tokens(retrieved_run.usage)
        print(f"Cost for this response: {cost_data}")
        insert_cost(session_id, cost_data)
    return thread_messages.data[0].content[0].text.value

def clear_cache(user_id):  
    records = get_user_chats(user_id)  
    
    # Check if records is None and set it to an empty list if it is  
    if records is None:  
        records = []  
    
    for record in records:  
        vector_id = record[2]
        file_id = record[4]
        print(vector_id)
        print(file_id)
        try:  
            # Ensure you pass the parameters correctly as dicts  
            openai_client.beta.vector_stores.delete(vector_store_id=vector_id)  
            openai_client.files.delete(file_id=file_id)  
        except Exception as e:  
            print(f"Error while deleting resources: {e}")  
    
    return

def cost_for_tokens(usage, model = "GPT-4o mini"):
    return usage.prompt_tokens * 0.15 / 1000000 + usage.completion_tokens * 0.6 / 1000000

def get_file_content(file_id):  
    # Retrieve file content
    try:  
        return openai_client.files.retrieve(file_id=file_id)
    except Exception as e:  
        print(f"Failed to retrieve file metadata: {e}")  
        return None