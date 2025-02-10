import streamlit as st
from github_module import clone_github_repo
from code_parser import parse_code
from neo4j_module import Neo4jHandler
from documentation_module import generate_documentation
from rag_module import ask_question
import openai

openai.api_key = "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"

def main():
    st.set_page_config(layout="wide")
    st.title("Automated Code Documentation and Query System")

    if 'parsed_data' not in st.session_state:
        st.session_state['parsed_data'] = None

    col1, col2 = st.columns([2, 3])

    with col1:
        st.header("Repository and Code Parsing")
        # Step 1: GitHub Repo Cloning
        repo_url = st.text_input("Enter GitHub Repository URL:", "https://github.com/dylanbuchi/31-days-of-code.git", key="repo_url")
        if st.button("Clone Repository"):
            clone_github_repo(repo_url)
            st.success("Repository cloned successfully.")

        # Step 2: Code Parsing
        if st.button("Parse Code"):
            st.session_state['parsed_data'] = parse_code()
            st.success("Code parsed successfully.")

        # Step 3: Neo4j Knowledge Graph Creation
        st.header("Knowledge Graph Creation")
        if st.button("Create Knowledge Graph"):
            handler = Neo4jHandler()
            if st.session_state['parsed_data'] is None:
                st.session_state['parsed_data'] = parse_code()
            with st.spinner('Creating knowledge graph, please wait...'):
                handler.create_nodes_and_relationships(st.session_state['parsed_data'])
            handler.close()
            st.success("Knowledge graph created successfully.")

    with col2:
        st.header("Chatbot and Documentation")
        # Step 4: Documentation Generation
        if st.button("Generate Documentation"):
            if st.session_state['parsed_data'] is None:
                st.session_state['parsed_data'] = parse_code()
            generate_documentation(st.session_state['parsed_data'])
            st.success("Documentation generated successfully.")

        # Step 5: Query Handling - Chatbot
        st.header("Ask Questions about the Codebase")
        query = st.text_input("Enter your question about the codebase:", key="user_query")
        if st.button("Answer Query"):
            answer = ask_question(query)
            st.success(f"Answer: {answer}")

if __name__ == "__main__":
    main()