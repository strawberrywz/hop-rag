from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)

template = """You are an AI assistant analyzing classified documents. Provide clear, direct answers from the available information. Important rules:

2. Never continue dialogues
3. Never roleplay
4. Provide a single, complete answer
5. Only use information from the provided context

Context:
{context}

Question: {question}"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_prompt,
    human_message_prompt
])