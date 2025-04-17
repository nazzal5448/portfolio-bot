import streamlit as st
from langchain_setup import output_parser, llm, prompt_template, build_qa_chain_with_memory
from langchain.memory import ConversationBufferMemory
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain

# Initialize memory for session
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

# Build chain using memory
qa_chain = build_qa_chain_with_memory(st.session_state.memory)

st.title("🧠 Portfolio Chatbot: Ask About Nazzal")

user_input = st.text_input("Ask a question about Nazzal:", "")

if user_input:
    result = qa_chain.invoke({"question": user_input})
    parsed_response = output_parser.invoke(result.get("result"))

    # Display result
    st.markdown(f"**🤖 Xel:** {parsed_response}")

    # Show chat history
    with st.expander("Chat History"):
        for msg in st.session_state.memory.chat_memory.messages:
            if msg.type == "human":
                st.markdown(f"**🧑 You:** {msg.content}")
            elif msg.type == "ai":
                st.markdown(f"**🤖 Xel:** {msg.content}")
