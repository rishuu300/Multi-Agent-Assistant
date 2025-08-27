import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with steramlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and display the output while
    implementing exception handling for robustness.
    """
    
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")
    
    if user_message:
        try:
            # Configure the LLM's
            obj_llm_config = GroqLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_models()
            
            if not model:
                st.error("Error: LLM model could not be initialized.")
                return
            
            # Initialize and set up the graph based on use case
            usecase = user_input.get('selected_usecase')
            
            if not usecase:
                st.error("Error: No usecase selected.")
            
            # Graph Builder
            graph_builder = GraphBuilder(model)
            
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed {e}")
                return
            
        except Exception as e:
            st.error(f"Error: Input processing failed {e}")
            return