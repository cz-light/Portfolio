import streamlit as st
import agent

def main(collection):
    st.set_page_config(page_title="EMTALA Legal Assistant", layout="wide", initial_sidebar_state="expanded")
    st.title("EMTALA Legal Assistant")

    if "history" not in st.session_state:
        st.session_state["history"] = []
    with st.form("query_form"):
        user_query = st.text_input("Enter your legal questions about EMTALA and cited cases or type \"quit\" to stop:")
        submitted = st.form_submit_button("Ask")

    if user_query == "quit":
        st.text("Session ended. Thank you for using the EMTALA Legal Assistant.")
        st.stop()

    if submitted and user_query.strip():
        if not agent.is_safe(user_query):
            st.warning("Your query was flagged as unsafe.")
        else:
            #query the collection
            retrieved_chunk, retrieved_meta = agent.retrieve_chunks(collection, user_query)
            #build complete prompt
            prompt = agent.build_augmented_prompt(user_query, retrieved_chunk, retrieved_meta, st.session_state["history"])
            answer = agent.get_llm_response(prompt)
            st.session_state["history"].append({"user": user_query, "assistant": answer})
            st.subheader("Answer")
            st.write(answer)

            st.subheader("Relevant Source Chunks")
            for i, chunk in enumerate(retrieved_chunk):
                st.markdown(f"Source {i+1}: {chunk}")

    if st.session_state["history"]:
        st.sidebar.header("Conversation History")
        for turn in st.session_state["history"]:
            st.sidebar.markdown(f"You: {turn['user']}")
            st.sidebar.markdown(f"Assistant: {turn['assistant']}")
