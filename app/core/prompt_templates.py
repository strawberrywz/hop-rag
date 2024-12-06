from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)

template = """ Summarize the context
Context: {context}
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_prompt,
    human_message_prompt
])