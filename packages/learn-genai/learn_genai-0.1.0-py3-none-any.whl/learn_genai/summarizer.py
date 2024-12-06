import streamlit as st
from langchain.llms import Ollama
from langchain.chains.summarize import load_summarize_chain

def run_summarizer():
    st.header("Text Summarizer")
    
    text = st.text_area("Enter the text to summarize:", height=200)
    
    if st.button("Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                llm = Ollama(model="llama2:3b")
                chain = load_summarize_chain(llm, chain_type="map_reduce")
                summary = chain.run(text)
                st.subheader("Summary:")
                st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")
