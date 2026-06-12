# app/streamlit_app.py
import sys
import os
import tempfile
from pathlib import Path
import streamlit as st

root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from pipeline.rag_pipeline import RAGPipeline
from pipeline.contracts import RiskLevel

st.set_page_config(
    page_title="ScamShield AI - Compliance Intel Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium styling injections tracking system layers
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1400px; }
    .risk-card { padding: 25px; border-radius: 8px; margin-bottom: 20px; color: white; font-weight: bold; }
    .safe-bg { background-color: #1b5e20; border-left: 8px solid #4caf50; }
    .suspicious-bg { background-color: #e65100; border-left: 8px solid #ff9800; }
    .scam-bg { background-color: #b71c1c; border-left: 8px solid #f44336; }
    .metric-box { background-color: #f8f9fa; border: 1px solid #e0e0e0; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 10px; }
    .metric-val { font-size: 1.6rem; font-weight: bold; color: #1e88e5; }
    .metric-lbl { font-size: 0.8rem; text-transform: uppercase; color: #616161; font-weight: 600; letter-spacing: 0.5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ ScamShield AI")
st.subheader("Fintech & Telecom Multi-Tenant Scam Risk Intelligence Engine")
st.caption("Production Readiness Verification Instance — Equipped with Multi-Stage System Telemetry Auditing")
st.divider()

if "pipeline" not in st.session_state:
    try:
        st.session_state.pipeline = RAGPipeline()
    except Exception as e:
        st.error(f"Failed to synchronize system engine topologies: {str(e)}")

# ==========================================
# SIDEBAR CONTROL PANELS (MULTI-TENANCY & STATS)
# ==========================================
with st.sidebar:
    st.header("🏢 Tenant Configuration")
    active_tenant = st.text_input(
        "Compliance Tenant Workspace ID",
        value="reliance_jio_compliance",
        help="Isolates document pools and query routing inside strict database namespaces."
    )
    
    st.divider()
    st.header("📂 Regulatory Data Ingestion")
    uploaded_file = st.file_uploader("Select Reference Asset", type=["pdf", "txt", "md"])
    
    if uploaded_file is not None:
        st.info(f"Asset Buffered: {uploaded_file.name}")
        if st.button("⚙️ Execute Ingestion Loop", use_container_width=True):
            with st.spinner("Executing layout extraction and multi-vector sync..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        temp_workspace_path = tmp.name
                    
                    report = st.session_state.pipeline.ingest_regulatory_document(
                        file_path=temp_workspace_path,
                        tenant_id=active_tenant
                    )
                    
                    if os.path.exists(temp_workspace_path):
                        os.remove(temp_workspace_path)
                        
                    if report.get("status") == "COMPLETED":
                        st.success("🎉 Ingestion Complete!")
                        st.markdown(f"""
                        <div style='background-color: #e3f2fd; padding: 15px; border-radius: 6px; border-left: 4px solid #2196f3; font-size:0.9rem;'>
                            <b>Ingestion Performance Telemetry:</b><br>
                            ⏱️ Parse Latency: {report['elapsed_ms']} ms<br>
                            📦 Section Chunks Generated: {report['chunks_processed']}<br>
                            📐 Avg Chunk Density: {report['avg_chunk_size_chars']} chars<br>
                            📊 Total Volume Loaded: {report['total_volume_chars']} chars
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Asset processed but contained no searchable entities.")
                except Exception as e:
                    st.error(f"Ingestion Sequence Aborted: {str(e)}")

# ==========================================
# MAIN APP EXECUTION WORKSPACE
# ==========================================
layout_left, layout_right = st.columns([1, 1], gap="large")

with layout_left:
    st.header("🔍 Incident Risk Verification")
    incident_payload = st.text_area(
        "Suspicious Interaction Content Input",
        height=220,
        placeholder="Paste text snippets here..."
    )
    run_analysis = st.button("🚀 Run Threat Assessment Run", use_container_width=True, type="primary")

with layout_right:
    st.header("📊 Structured Verdict Outcome Dashboard")
    
    if run_analysis and incident_payload.strip():
        with st.spinner("Executing hybrid retrieval loops and structured analytics checks..."):
            
            # Fire orchestrated check returning our combined payload dict
            pipeline_output = st.session_state.pipeline.analyze_incident(
                query_text=incident_payload,
                tenant_id=active_tenant
            )
            
            verdict_report = pipeline_output["verdict"]
            telemetry = pipeline_output["telemetry"]
            
            # Dynamic color styling selectors
            if verdict_report.verdict == RiskLevel.SAFE:
                bg_class, icon = "safe-bg", "✅"
            elif verdict_report.verdict == RiskLevel.SUSPICIOUS:
                bg_class, icon = "suspicious-bg", "⚠️"
            else:
                bg_class, icon = "scam-bg", "🚨"
                
            # Render main status verification card
            st.markdown(f"""
                <div class='risk-card {bg_class}'>
                    <h3 style='margin:0; color:white;'>{icon} EVALUATION VERDICT: {verdict_report.verdict.value}</h3>
                    <p style='margin:5px 0 0 0; font-size: 1.1rem; color:#f5f5f5;'>Calculated Severity Index: {verdict_report.risk_score:.2f} / 1.00</p>
                </div>
            """, unsafe_allow_html=True)
            
            # ==========================================
            # ⚡ HIGH-VALUE SYSTEM TELEMETRY PANEL ⚡
            # ==========================================
            st.subheader("⚡ Core RAG Infrastructure Telemetry")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{telemetry['total_pipeline_latency_ms']}ms</div><div class='metric-lbl'>Total Latency</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{telemetry['retrieval_dense_sparse_ms']}ms</div><div class='metric-lbl'>Qdrant Vector Engine</div></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{telemetry['reranking_cross_encoder_ms']}ms</div><div class='metric-lbl'>Cross-Encoder</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{telemetry['llm_generation_ms']}ms</div><div class='metric-lbl'>70B Inference</div></div>", unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{telemetry['active_knowledge_base_pdfs']}</div><div class='metric-lbl'>Validated PDFs</div></div>", unsafe_allow_html=True)
                audit_color = "#2e7d32" if "PASSED" in telemetry['hallucination_audit_status'] else "#c62828"
                st.markdown(f"<div class='metric-box'><div class='metric-val' style='color:{audit_color}; font-size:1.1rem; padding-top:6px;'>{telemetry['hallucination_audit_status']}</div><div class='metric-lbl'>Hallucination Audit</div></div>", unsafe_allow_html=True)

            st.caption(f"**Context Filtering Volumetrics:** {telemetry['candidate_pool_reduction']}")
            st.markdown(f"**Incident Core Profile:** {verdict_report.input_text_summary}")
            st.divider()
            
            # Reasoning checklist structures
            st.subheader("🧠 System Reasoning Analysis Traces")
            for trace in verdict_report.reasoning_breakdown:
                st.markdown(f"- {trace}")
                
            st.divider()
            # Recommended Measures lists
            st.subheader("🛡️ Strategic Mitigation Actions")
            for action in verdict_report.recommended_actions:
                st.markdown(f"📍 **{action}**")
                
            st.divider()
            # Granular Citations presentation lists
            st.subheader("📄 Regulatory Lineage Verifications")
            if verdict_report.regulatory_citations:
                for idx, cite in enumerate(verdict_report.regulatory_citations):
                    with st.expander(f"Citation {idx + 1}: {cite.source_document} — Reference: {cite.clause_reference}"):
                        st.markdown(f"**Analytical Context Rationale:** *{cite.relevance_rationale}*")
                        st.caption("Verbatim Regulatory Context Rule Block:")
                        st.code(cite.matched_text_context, language="markdown")
            else:
                st.info("No explicit data assets were referenced for this safe risk outcome profile.")
                
    elif run_analysis:
        st.warning("Please provide an active raw text payload snippet string inside the input console before initializing verification sequences.")
    else:
        st.info("📌 Awaiting input metrics. Insert criteria and click 'Run Threat Assessment Run' to verify parameters.")