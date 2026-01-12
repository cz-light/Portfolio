from openai import OpenAI
import os

ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = 'gpt-4o-mini'
convo_history = []

def build_augmented_prompt(user_query, retrieved_chunks, retrieved_metadata, history): 
    #revamp prompt
    system_prompt = """You are a helpful chatbot that assists lawyers, physicians, and other medical staff with understanding the penalties 
    for infractions and violations of the Emergency Medical Treatment and Labor Act (EMTALA). You are a legal expert in this field and 
    can provide detailed information about the law, its implications, and the penalties associated with violations. Your tone is professional 
    and informative, and you should avoid providing personal opinions or legal advice. Always refer to the law and its provisions when answering 
    questions. You may make inferences based on the law, but you should always state that you are making an inference and how you came to that conclusion. 
    When answering, ALWAYS use the provided 'Relevant information from documents' and their 'Metadata' as your primary sources. Reference specific details 
    (such as hospital name, date, state, or penalty amount) from the sources when possible. If you cannot answer from the provided sources, say so."""
    
    context = "\n\n".join([f"Source: {chunk}\nMetadata: {data}" for chunk,data in zip(retrieved_chunks, retrieved_metadata)])
    history_text = "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history])
    prompt = (
        f"{system_prompt}\n\n"
        f"Relevant information from documents:\n{context}\n\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"User question: {user_query}\n"
        f"Answer:"
    )
    return prompt

def is_safe(user_input): 
    response = ai_client.moderations.create(
        model="omni-moderation-latest",
        input=user_input
    )
    return not response.results[0].flagged


def retrieve_chunks(collection, query, k=100): 
    results = collection.query(
        query_texts=[query],
        #n_results=k,
        include=["documents", "metadatas"]
    )
    #return the top-k document texts
    return results["documents"][0], results["metadatas"][0]

def get_llm_response(prompt): 
    response = ai_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

