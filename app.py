from packages import *
from graph import builder
from nodes import AgentState
import streamlit as st
import time
 
# Make sure to import your compiled LangGraph + state


def main():
    # Title
    st.title("🔎 Smart Web Search Agent")

    # Session state to hold output and steps, start of a session
    if "response" not in st.session_state:
        st.session_state.response = ""
        st.session_state.steps = []
    
    if "graph" not in st.session_state:
        # Initialize the state graph
        st.session_state.graph = builder.build()

    # Input
    with st.form("query_form"):
        query = st.text_input("Enter your search query", "")
        submitted = st.form_submit_button("Search")

    # Run LangGraph on form submission
    if submitted:
        # print(f"Running search for query: {query}")
        def run():
            # steps = []
            initial_state = AgentState(query=query)
            def run_graph():
                for state in st.session_state.graph.stream(initial_state):
                    pass
                return state

            time.sleep(30)
            final_state =  run_graph()
            st.session_state.response = final_state
            # st.session_state.steps = steps
        run()

    # Output
    if st.session_state.response:
        st.subheader("✅ Final Answer")
        st.write(st.session_state.response)


    # Reset Button
    if st.button("🔄 Reset"):
        st.session_state.response = ""
        st.session_state.steps = []
        st.experimental_rerun()



if __name__ == "__main__":
    main()