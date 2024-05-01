import streamlit as st
from model.get_examples import vector_search

def example_input(prompt):
    example_auto = st.toggle("Auto-generate examples?")
    example_list = {"request":[],
                "response":[]}
    if example_auto:
        @st.cache_resource
        def search_example(prompt, n=10):
            search = vector_search()
            top_problems, top_solutions = search.compute_search(prompt, n)
            return top_problems, top_solutions
        top_problems, top_solutions = search_example(prompt, 5)
        chosen_problem = [False]*len(top_problems)
        for i in range(len(top_problems)):
            container = st.columns([0.05,0.35,0.6])
            chosen_problem[i] = container[0].checkbox(f"example {i+1}", label_visibility="collapsed")
            with container[1].expander(f"{top_problems.iloc[i][:30]}..."):
                st.write(top_problems.iloc[i])
            with container[2].expander("See the query"):
                st.text(top_solutions.iloc[i])
            if chosen_problem[i]:
                example_list["request"].append(top_problems.iloc[i])
                example_list["response"].append(top_solutions.iloc[i])
                
    add_example = st.toggle("Mannually enter your example?")
    if add_example:
        example_cols = st.columns([0.3,0.7])
        example_request = example_cols[0].text_area("Example Request", height=5)
        example_response = example_cols[1].text_area("Example Response", height=5)
        example_list["request"].append(example_request)
        example_list["response"].append(example_response)
    return example_list