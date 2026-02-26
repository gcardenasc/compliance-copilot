import streamlit as st
from api_client import ComplianceAPIClient

st.set_page_config(
    page_title="Regulatory Analysis Workbench",
    page_icon="⚖️",
    layout="wide"
)

# Load CSS
with open("ui/styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

api = ComplianceAPIClient()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Document Repository")
    uploaded_file = st.file_uploader("Upload Regulation", type=["pdf", "docx"])
    if uploaded_file:
        with st.spinner("Indexing document..."):
            res = api.upload_file(uploaded_file)
            st.success(f"ID: {res.get('doc_id')}")
            st.session_state.doc_id = res.get('doc_id')

    st.divider()
    st.header("⚙️ Configuration")
    strict_mode = st.toggle("Strict Compliance Mode", value=True, help="Only answers if explicit support exists in the text.")
    threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7)

    st.divider()
    st.markdown("### 🔗 Project Links")
    st.markdown("[GitHub Repository](https://github.com/gcardenasc/compliance-copilot/tree/feature/cloud-hybrid-llm)")

# --- MAIN INTERFACE ---
st.title("⚖️ Regulatory Analysis Workbench")
st.caption("Agentic-RAG System for Compliance and Risk Analysis")

query = st.text_input("Enter regulatory query or specific article analysis request:", placeholder="e.g., ¿Cuáles son los requisitos de reporting para el artículo 14?")

if query:
    if not st.session_state.get('doc_id'):
        st.error("Please upload or select a document in the repository first.")
    else:
        with st.spinner("Executing agentic reasoning..."):
            # Lógica de llamada al agente
            response = api.ask_question(query, st.session_state.doc_id, strict_mode)
            
            # --- DISPLAY RESULTS ---
            col1, col2 = st.columns([0.7, 0.3])
            
            with col1:
                st.subheader("Technical Analysis")
                st.markdown(response.get("answer", "No analysis generated."))
                
                st.divider()
                st.subheader("Reference Citations")
                for cite in response.get("citations", []):
                    with st.container():
                        st.markdown(f"""
                        <div class="citation-card">
                            <strong>Article:</strong> {cite.get('article', 'N/A')} | 
                            <strong>Page:</strong> {cite.get('page', 'N/A')} | 
                            <strong>Score:</strong> {cite.get('score', '0.0')}
                            <br>
                            <em>"{cite.get('excerpt', 'No excerpt provided.')}"</em>
                        </div>
                        """, unsafe_allow_html=True)

            with col2:
                st.subheader("Metrics")
                conf = response.get("confidence", 0.0)
                conf_class = "confidence-high" if conf > 0.8 else "confidence-mid" if conf > 0.5 else "confidence-low"
                
                st.metric("Confidence Score", f"{conf*100:.1f}%")
                st.markdown(f"Status: <span class='{conf_class}'>{'VERIFIED' if conf > 0.7 else 'CAUTION'}</span>", unsafe_allow_html=True)
                
                with st.expander("Technical Reasoning (Chain of Thought)"):
                    thoughts = response.get("thoughts")
                    if thoughts:
                        st.markdown(thoughts)
                    else:
                        st.caption("No internal reasoning captured for this turn.")
