import os
import io
import json
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Set Page Config
st.set_page_config(
    page_title="TeaCare AI - Tea Leaf Disease Detection System",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
<style>
    /* Main Theme Styling */
    .main {
        background-color: #f8faf9;
    }
    h1, h2, h3 {
        color: #1e3a29;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Card Container */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e8e3;
        margin-bottom: 15px;
    }
    
    /* Result Header */
    .result-box {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 24px;
        border-left: 8px solid #2ecc71;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* Severity Badges */
    .badge-high {
        background-color: #fde8e8;
        color: #9b1c1c;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #f8b4b4;
    }
    .badge-mod {
        background-color: #feecdc;
        color: #9a3412;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #fbd5d5;
    }
    .badge-healthy {
        background-color: #def7ec;
        color: #03543f;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #84e1bc;
    }
    
    /* Advisory Accordions */
    .stAccordion > div {
        border-radius: 8px;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Helper to load predictor safely
@st.cache_resource
def load_model_engine():
    try:
        from src.predictor import get_predictor
        return get_predictor(), None
    except Exception as e:
        return None, str(e)

def main():
    # Sidebar Header
    st.sidebar.image("https://img.icons8.com/color/96/tea-leaf.png", width=70)
    st.sidebar.title("TeaCare AI System")
    st.sidebar.caption("AI-Based Tea Leaf Disease Detection & Management Platform")
    st.sidebar.markdown("---")
    
    navigation = st.sidebar.radio(
        "Navigation Menu",
        [
            "🍃 Single Leaf Diagnosis",
            "📦 Batch Diagnosis",
            "📊 Analytics & Performance",
            "📖 Disease Catalog & Guide",
            "ℹ️ About & Project Info"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**ICBT / CMU Research Project**\n\n"
        "Detects 8 conditions:\n"
        "• Anthracnose\n"
        "• Algal Leaf Spot\n"
        "• Bird's Eye Spot\n"
        "• Brown Blight\n"
        "• Gray Light\n"
        "• Healthy Leaf\n"
        "• Red Leaf Spot\n"
        "• White Spot"
    )
    
    predictor, err = load_model_engine()
    
    # ----------------------------------------------------
    # Page 1: Single Leaf Diagnosis
    # ----------------------------------------------------
    if navigation == "🍃 Single Leaf Diagnosis":
        st.title("🍃 Tea Leaf Disease Diagnosis")
        st.write("Upload an image of a tea leaf or use your camera to receive real-time disease detection, severity assessment, and agronomist remedies.")
        
        if predictor is None:
            st.error(f"⚠️ Model Engine Unavailable: {err}")
            st.info("Please complete model training by running `python train_model.py` in the workspace.")
            return

        col_input, col_display = st.columns([1, 1])
        
        with col_input:
            input_mode = st.radio("Choose Input Method", ["Upload Image File", "Use Camera Capture"], horizontal=True)
            uploaded_file = None
            
            if input_mode == "Upload Image File":
                uploaded_file = st.file_uploader(
                    "Drop tea leaf image here (JPG, PNG, WEBP)",
                    type=["jpg", "jpeg", "png", "webp"],
                    help="Upload a clear close-up photograph of the affected tea leaf."
                )
            else:
                uploaded_file = st.camera_input("Capture Tea Leaf Image")
                
            if uploaded_file is not None:
                try:
                    img_preview = Image.open(uploaded_file).convert("RGB")
                    st.image(img_preview, caption="Uploaded Leaf Image", use_container_width=True)
                except Exception as ex:
                    st.error(f"Failed to display image: {ex}")
                    
        with col_display:
            if uploaded_file is not None:
                with st.spinner("Analyzing image features & running neural network inference..."):
                    uploaded_file.seek(0)
                    result = predictor.predict(uploaded_file)
                    
                if not result['success']:
                    st.error(f"❌ Image Validation Failed: {result['error']}")
                else:
                    disp_name = result['predicted_class_display']
                    conf = result['confidence_percentage']
                    advisory = result['advisory']
                    severity = advisory.get('severity', 'Moderate')
                    
                    # Severity Pill Badge
                    if "Healthy" in disp_name:
                        badge_html = f'<span class="badge-healthy">SEVERITY: NONE (HEALTHY)</span>'
                        border_color = "#2ecc71"
                    elif severity in ['High', 'Severe']:
                        badge_html = f'<span class="badge-high">SEVERITY: HIGH</span>'
                        border_color = "#e74c3c"
                    else:
                        badge_html = f'<span class="badge-mod">SEVERITY: MODERATE</span>'
                        border_color = "#e67e22"
                        
                    st.markdown(f"""
                    <div class="result-box" style="border-left-color: {border_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="margin:0; color:#1e3a29;">{disp_name}</h2>
                            {badge_html}
                        </div>
                        <h3 style="margin-top:10px; color:#27ae60;">Confidence: {conf}%</h3>
                        <p style="color:#555; font-size:14px; margin-bottom:0;">
                            <b>Biological Cause:</b> {advisory.get('cause', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if result.get('domain_warning'):
                        st.warning(f"⚠️ {result['domain_warning']}")
                        
                    # Plotly Confidence Bar Chart
                    df_probs = pd.DataFrame(result['class_probabilities'])
                    fig = px.bar(
                        df_probs.head(5),
                        x='percentage',
                        y='display_name',
                        orientation='h',
                        text='percentage',
                        labels={'percentage': 'Probability (%)', 'display_name': 'Disease Class'},
                        color='percentage',
                        color_continuous_scale='Greens',
                        title="Top Class Probability Breakdown"
                    )
                    fig.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        height=240,
                        margin=dict(l=0, r=20, t=35, b=0),
                        showlegend=False
                    )
                    fig.update_traces(texttemplate='%{text}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                    
        # Detailed Agronomist Advisory Section
        if uploaded_file is not None and result.get('success'):
            st.markdown("---")
            st.subheader("📋 Agronomist Disease Management & Treatment Guide")
            
            tab_sym, tab_org, tab_chem, tab_prev, tab_rep = st.tabs([
                "🔍 Symptoms & Cause",
                "🌿 Organic Control",
                "🧪 Chemical Treatment",
                "🛡️ Prevention",
                "📄 Diagnostic Report"
            ])
            
            with tab_sym:
                st.markdown(f"**Biological Pathogen:** {advisory.get('cause')}")
                st.markdown("**Observed Clinical Symptoms:**")
                for s in advisory.get('symptoms', []):
                    st.markdown(f"- {s}")
                    
            with tab_org:
                st.markdown("**Eco-Friendly & Organic Remedies:**")
                for o in advisory.get('organic_treatment', []):
                    st.markdown(f"- 🍃 {o}")
                    
            with tab_chem:
                st.markdown("**Targeted Chemical Fungicide Spraying:**")
                for c in advisory.get('chemical_treatment', []):
                    st.markdown(f"- 🧪 {c}")
                    
            with tab_prev:
                st.markdown("**Cultural & Agricultural Preventive Measures:**")
                for p in advisory.get('prevention', []):
                    st.markdown(f"- 🛡️ {p}")
                    
            with tab_rep:
                from src.report_generator import generate_diagnostic_report_text
                report_txt = generate_diagnostic_report_text(result)
                st.text_area("Full Diagnostic Report Text", report_txt, height=260)
                st.download_button(
                    label="📥 Download Diagnostic Report (.txt)",
                    data=report_txt,
                    file_name=f"tea_leaf_report_{result['predicted_class_raw']}.txt",
                    mime="text/plain"
                )

    # ----------------------------------------------------
    # Page 2: Batch Diagnosis
    # ----------------------------------------------------
    elif navigation == "📦 Batch Diagnosis":
        st.title("📦 Batch Tea Leaf Image Processing")
        st.write("Upload multiple leaf photos simultaneously to analyze field samples in bulk and export structured reports.")
        
        if predictor is None:
            st.error(f"⚠️ Model Engine Unavailable: {err}")
            return
            
        batch_files = st.file_uploader(
            "Select multiple tea leaf images",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True
        )
        
        if batch_files:
            st.info(f"Loaded {len(batch_files)} images for analysis.")
            if st.button("🚀 Process All Batch Samples", type="primary"):
                results_list = []
                progress_bar = st.progress(0)
                
                for idx, file_obj in enumerate(batch_files):
                    file_obj.seek(0)
                    res = predictor.predict(file_obj)
                    
                    if res['success']:
                        results_list.append({
                            'Filename': file_obj.name,
                            'Predicted Disease': res['predicted_class_display'],
                            'Confidence (%)': res['confidence_percentage'],
                            'Severity': res['advisory'].get('severity', 'N/A'),
                            'Validation Status': res['validation_status'],
                            'Domain Check': 'PASS' if res['is_leaf_like'] else 'WARNING'
                        })
                    else:
                        results_list.append({
                            'Filename': file_obj.name,
                            'Predicted Disease': 'FAILED',
                            'Confidence (%)': 0.0,
                            'Severity': 'N/A',
                            'Validation Status': res['error'],
                            'Domain Check': 'FAIL'
                        })
                    progress_bar.progress((idx + 1) / len(batch_files))
                    
                df_results = pd.DataFrame(results_list)
                st.success("✅ Batch processing completed successfully!")
                
                st.dataframe(df_results, use_container_width=True)
                
                # CSV Export
                csv_buffer = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Batch Summary CSV",
                    data=csv_buffer,
                    file_name="batch_tea_disease_summary.csv",
                    mime="text/csv"
                )

    # ----------------------------------------------------
    # Page 3: Analytics & Performance Dashboard
    # ----------------------------------------------------
    elif navigation == "📊 Analytics & Performance":
        st.title("📊 Model Performance & Dataset Analytics")
        st.write("Quantitative evaluation of the deep learning model trained on 885 tea leaf images across 8 disease classes.")
        
        meta_path = os.path.join("models", "model_metadata.json")
        cm_path = os.path.join("models", "confusion_matrix.png")
        hist_path = os.path.join("models", "training_history.png")
        
        if not os.path.exists(meta_path):
            st.warning("Model metadata file not found. Please run training script `python train_model.py` first.")
            return
            
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
            
        test_m = metadata.get('test_metrics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Accuracy", f"{test_m.get('accuracy', 0)*100:.2f}%")
        col2.metric("Weighted Precision", f"{test_m.get('precision', 0)*100:.2f}%")
        col3.metric("Weighted Recall", f"{test_m.get('recall', 0)*100:.2f}%")
        col4.metric("Weighted F1-Score", f"{test_m.get('f1_score', 0)*100:.2f}%")
        
        st.markdown("---")
        
        col_cm, col_hist = st.columns([1, 1])
        with col_cm:
            st.subheader("Confusion Matrix")
            if os.path.exists(cm_path):
                st.image(cm_path, use_container_width=True)
            else:
                st.info("Confusion matrix image not generated.")
                
        with col_hist:
            st.subheader("Training & Validation Curves")
            if os.path.exists(hist_path):
                st.image(hist_path, use_container_width=True)
            else:
                st.info("Training history plot not generated.")
                
        st.markdown("---")
        st.subheader("Dataset Class Distribution")
        counts = metadata.get('dataset_counts', {})
        if counts:
            df_counts = pd.DataFrame(list(counts.items()), columns=['Disease Class', 'Sample Count'])
            fig_counts = px.bar(
                df_counts, x='Disease Class', y='Sample Count',
                color='Sample Count', color_continuous_scale='Viridis',
                title="Images per Class in Dataset (Total: 885)"
            )
            st.plotly_chart(fig_counts, use_container_width=True)

    # ----------------------------------------------------
    # Page 4: Disease Catalog & Guide
    # ----------------------------------------------------
    elif navigation == "📖 Disease Catalog & Guide":
        st.title("📖 Tea Leaf Disease Catalog")
        st.write("Browse comprehensive disease profiles, visual symptoms, and treatment guidelines for all 8 categories.")
        
        from src.advisory import DISEASE_ADVISORY_DB
        
        selected_key = st.selectbox(
            "Select Tea Leaf Condition to Inspect",
            list(DISEASE_ADVISORY_DB.keys())
        )
        
        info = DISEASE_ADVISORY_DB[selected_key]
        
        st.markdown(f"## {info['display_name']}")
        st.markdown(f"**Severity Level:** {info['severity']} | **Pathogen / Cause:** {info['cause']}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔍 Clinical Symptoms")
            for s in info['symptoms']:
                st.markdown(f"- {s}")
                
            st.subheader("🌿 Organic Remedies")
            for o in info['organic_treatment']:
                st.markdown(f"- {o}")
                
        with c2:
            st.subheader("🧪 Chemical Controls")
            for c in info['chemical_treatment']:
                st.markdown(f"- {c}")
                
            st.subheader("🛡️ Cultural Prevention")
            for p in info['prevention']:
                st.markdown(f"- {p}")

    # ----------------------------------------------------
    # Page 5: About & Project Info
    # ----------------------------------------------------
    elif navigation == "ℹ️ About & Project Info":
        st.title("ℹ️ Project & Research Documentation")
        
        st.markdown("""
        ### AI-Based Tea Leaf Disease Detection System Using Deep Learning
        **Academic Institution:** International College of Business and Technology (ICBT) / Cardiff Metropolitan University  
        **Author:** D M Tharushi Nilasha Dasanayaka  
        **Student ID:** ST20283758 (CL/BSCDS/CMU/09/68)  
        
        ---
        
        ### Executive Summary
        Tea (*Camellia sinensis*) is a critical commercial crop and key driver of agricultural revenue in Sri Lanka. 
        Leaf diseases such as Blister Blight, Anthracnose, Algal Leaf Spot, Grey Blight, and Brown Blight cause severe crop loss if left undetected. 
        Traditional manual field inspection is labor-intensive, slow, and prone to diagnostic error.
        
        This AI system delivers an automated, deep learning platform leveraging **Custom Residual Neural Networks (CNNs)** 
        and computer vision to instantly classify tea leaf diseases, evaluate image validity, and output actionable agronomist treatment plans.
        
        ### Core Features
        - **Multi-Class Neural Classification**: Trained on 8 dataset classes with image augmentations.
        - **Automated Image Validation**: Checks resolution, corruption, and plant foliage color distribution (HSV histogram check).
        - **Agronomist Advisory Engine**: Outlines biological causes, organic controls, chemical sprays, and preventive field practices.
        - **Batch Diagnosis & Export**: Enables rapid bulk analysis for large plantation estates.
        - **Performance Visualizer**: Integrated confusion matrix and loss/accuracy curves.
        """)

if __name__ == '__main__':
    main()

