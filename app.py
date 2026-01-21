"""
🔍 AIGovLens - Open Source AI Governance Toolkit
Evaluate AI use cases against regulatory frameworks and generate compliance reports.

Author: Parul Khanna
License: MIT
GitHub: github.com/parul-khanna/aigovlens
"""

import streamlit as st
import json
from datetime import datetime
from groq import Groq
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="AIGovLens - AI Governance Toolkit",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0;
    }
    .main-header span {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .tagline {
        font-size: 1.1rem;
        color: #64748B;
        margin-top: 0.5rem;
    }

    /* Score cards */
    .score-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-value {
        font-size: 3rem;
        font-weight: 700;
    }
    .score-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    /* Risk badges */
    .risk-high { background: #FEE2E2; color: #DC2626; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .risk-medium { background: #FEF3C7; color: #D97706; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .risk-low { background: #D1FAE5; color: #059669; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }

    /* Cards */
    .info-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .info-card h4 {
        margin: 0 0 0.5rem 0;
        color: #1E293B;
    }
    .info-card p {
        margin: 0;
        color: #64748B;
        font-size: 0.9rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# EVALUATION PROMPT
# ============================================================================
EVALUATION_PROMPT = """You are an expert AI governance analyst. Evaluate the following AI use case against regulatory frameworks and risk criteria.

## USE CASE DETAILS:
Name: {name}
Department: {department}
Description: {description}
AI Techniques: {ai_techniques}
Target Markets: {markets}
Data Types: {data_types}
Deployment Stage: {stage}

## EVALUATE AGAINST:
1. **Regulatory Risk**: EU AI Act, Colorado AI Act, NYC Local Law 144, GDPR implications
2. **Bias & Fairness Risk**: Potential for discrimination, affected groups, historical bias in domain
3. **Data Privacy Risk**: PII handling, consent, data retention, cross-border transfers
4. **Transparency Risk**: Explainability requirements, user notification, right to human review

## RETURN JSON ONLY (no markdown, no explanation outside JSON):
{{
    "overall_score": <0-100 integer>,
    "risk_level": "<HIGH|MEDIUM|LOW>",
    "risks": {{
        "regulatory": {{
            "level": "<HIGH|MEDIUM|LOW>",
            "score": <0-100>,
            "summary": "<2-3 sentence explanation>",
            "applicable_regulations": ["<list of specific regulations that apply>"]
        }},
        "bias": {{
            "level": "<HIGH|MEDIUM|LOW>",
            "score": <0-100>,
            "summary": "<2-3 sentence explanation>",
            "affected_groups": ["<list of potentially affected groups>"]
        }},
        "privacy": {{
            "level": "<HIGH|MEDIUM|LOW>",
            "score": <0-100>,
            "summary": "<2-3 sentence explanation>",
            "data_concerns": ["<list of specific data concerns>"]
        }},
        "transparency": {{
            "level": "<HIGH|MEDIUM|LOW>",
            "score": <0-100>,
            "summary": "<2-3 sentence explanation>",
            "requirements": ["<list of transparency requirements>"]
        }}
    }},
    "recommended_actions": [
        {{
            "priority": 1,
            "action": "<specific action to take>",
            "regulation": "<relevant regulation or best practice>",
            "owner": "<suggested responsible party>"
        }}
    ],
    "executive_summary": "<3-4 sentence summary suitable for leadership>"
}}
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_risk_badge(level):
    """Return HTML for risk level badge"""
    level = level.upper()
    if level == "HIGH":
        return '<span class="risk-high">⚠️ HIGH</span>'
    elif level == "MEDIUM":
        return '<span class="risk-medium">⚡ MEDIUM</span>'
    else:
        return '<span class="risk-low">✅ LOW</span>'


def evaluate_use_case(use_case_data, api_key):
    """Send use case to Groq for evaluation"""
    try:
        client = Groq(api_key=api_key)

        prompt = EVALUATION_PROMPT.format(
            name=use_case_data['name'],
            department=use_case_data['department'],
            description=use_case_data['description'],
            ai_techniques=use_case_data['ai_techniques'],
            markets=', '.join(use_case_data['markets']),
            data_types=', '.join(use_case_data['data_types']),
            stage=use_case_data['stage']
        )

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an AI governance expert. Return only valid JSON, no markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        result_text = response.choices[0].message.content.strip()

        # Clean up response if it has markdown code blocks
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        result_text = result_text.strip()

        return json.loads(result_text)

    except json.JSONDecodeError as e:
        st.error(f"Failed to parse AI response. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")
        return None


def generate_pdf_report(use_case_data, evaluation_result):
    """Generate a professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1E293B'), spaceAfter=6)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#64748B'), spaceAfter=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#3B82F6'), spaceBefore=20, spaceAfter=10)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#374151'), spaceAfter=8)

    # Header
    story.append(Paragraph("🔍 AIGovLens Governance Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3B82F6')))
    story.append(Spacer(1, 20))

    # Use Case Overview
    story.append(Paragraph("📋 Use Case Overview", heading_style))
    overview_data = [
        ["Use Case Name:", use_case_data['name']],
        ["Department:", use_case_data['department']],
        ["AI Techniques:", use_case_data['ai_techniques']],
        ["Deployment Stage:", use_case_data['stage']],
        ["Target Markets:", ', '.join(use_case_data['markets'])],
        ["Data Types:", ', '.join(use_case_data['data_types'])]
    ]
    overview_table = Table(overview_data, colWidths=[1.5*inch, 5*inch])
    overview_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748B')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Description:", ParagraphStyle('Label', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#64748B'))))
    story.append(Paragraph(use_case_data['description'], body_style))

    # Overall Assessment
    story.append(Paragraph("📊 Overall Assessment", heading_style))
    risk_color = {'HIGH': '#DC2626', 'MEDIUM': '#D97706', 'LOW': '#059669'}.get(evaluation_result['risk_level'], '#64748B')
    assessment_data = [
        ["Overall Score:", f"{evaluation_result['overall_score']}/100"],
        ["Risk Level:", evaluation_result['risk_level']]
    ]
    assessment_table = Table(assessment_data, colWidths=[1.5*inch, 5*inch])
    assessment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748B')),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor(risk_color)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(assessment_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph(evaluation_result.get('executive_summary', ''), body_style))

    # Risk Breakdown
    story.append(Paragraph("⚠️ Risk Assessment", heading_style))
    risks = evaluation_result.get('risks', {})

    for risk_name, risk_data in risks.items():
        risk_title = risk_name.replace('_', ' ').title()
        level = risk_data.get('level', 'UNKNOWN')
        level_color = {'HIGH': '#DC2626', 'MEDIUM': '#D97706', 'LOW': '#059669'}.get(level, '#64748B')

        story.append(Paragraph(f"<b>{risk_title} Risk:</b> <font color='{level_color}'>{level}</font>", body_style))
        story.append(Paragraph(risk_data.get('summary', ''), body_style))
        story.append(Spacer(1, 8))

    # Recommended Actions
    story.append(Paragraph("✅ Recommended Actions", heading_style))
    actions = evaluation_result.get('recommended_actions', [])

    if actions:
        action_data = [["Priority", "Action", "Regulation", "Owner"]]
        for action in actions[:6]:  # Limit to 6 actions
            action_data.append([
                f"P{action.get('priority', '-')}",
                action.get('action', '')[:60],
                action.get('regulation', '')[:30],
                action.get('owner', '')
            ])

        action_table = Table(action_data, colWidths=[0.6*inch, 3*inch, 1.5*inch, 1.4*inch])
        action_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(action_table)

    # Footer
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0')))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#94A3B8'), alignment=TA_CENTER)
    story.append(Paragraph("Generated by AIGovLens - Open Source AI Governance Toolkit", footer_style))
    story.append(Paragraph("github.com/parul-khanna/aigovlens | MIT License", footer_style))
    story.append(Paragraph("⚠️ This report is for informational purposes only and does not constitute legal advice.", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔍 AIGovLens")
        st.markdown("*See AI risks clearly*")
        st.markdown("---")

        # API Key input
        st.markdown("### 🔑 API Configuration")

        # Check for API key in secrets or session state
        api_key = ""
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            api_key = st.secrets['GROQ_API_KEY']
            st.success("✅ API key loaded from secrets")
        else:
            api_key = st.text_input(
                "Groq API Key",
                type="password",
                placeholder="gsk_...",
                help="Get free API key at console.groq.com"
            )
            if api_key:
                st.success("✅ API key entered")
            else:
                st.warning("⚠️ Enter API key to evaluate")
                st.markdown("[Get free Groq API key →](https://console.groq.com)")

        st.markdown("---")

        st.markdown("### 📚 About")
        st.markdown("""
        AIGovLens evaluates AI use cases against:
        - 🏛️ EU AI Act
        - 🇺🇸 Colorado AI Act
        - 🗽 NYC Local Law 144
        - 🔒 GDPR & Privacy
        - ⚖️ Bias & Fairness
        """)

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #64748B;">
            <b>MIT License</b><br>
            Built by <a href="https://linkedin.com/in/yourprofile">Parul Khanna</a>
        </div>
        """, unsafe_allow_html=True)

    # Main content
    st.markdown('<h1 class="main-header">🔍 <span>AIGovLens</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Open source AI governance toolkit — Evaluate use cases against regulatory frameworks</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Initialize session state
    if 'evaluation_result' not in st.session_state:
        st.session_state.evaluation_result = None
    if 'use_case_data' not in st.session_state:
        st.session_state.use_case_data = None

    # Tabs
    tab1, tab2 = st.tabs(["📝 Evaluate Use Case", "📊 Results"])

    with tab1:
        st.markdown("### Enter Use Case Details")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Use Case Name *",
                placeholder="e.g., Customer Churn Prediction Model"
            )

            department = st.selectbox(
                "Department / Business Unit",
                ["Select...", "Human Resources", "Finance", "Operations", "Customer Service",
                 "Marketing", "Sales", "IT / Technology", "Legal", "Risk & Compliance", "Other"]
            )

            ai_techniques = st.selectbox(
                "AI/ML Techniques",
                ["Select...", "Machine Learning (Classification/Regression)", "Natural Language Processing (NLP)",
                 "Generative AI / Large Language Models", "Computer Vision", "Recommendation Systems",
                 "Robotic Process Automation (RPA)", "Predictive Analytics", "Multiple / Hybrid"]
            )

        with col2:
            stage = st.selectbox(
                "Deployment Stage",
                ["Select...", "Ideation / Concept", "Development / POC", "Pilot / Testing",
                 "Production (Limited)", "Production (Full Scale)"]
            )

            markets = st.multiselect(
                "Target Markets / Jurisdictions *",
                ["United States", "European Union", "Canada", "United Kingdom",
                 "Asia Pacific", "Latin America", "Global"],
                default=[]
            )

            data_types = st.multiselect(
                "Data Types Involved *",
                ["Personal Identifiable Information (PII)", "Employee / HR Data",
                 "Financial Data", "Health Information", "Biometric Data",
                 "Customer Behavior Data", "Public Data Only", "Synthetic / Anonymized"],
                default=[]
            )

        description = st.text_area(
            "Use Case Description *",
            placeholder="""Describe what this AI system will do:
- What problem does it solve?
- What decisions will it make or support?
- Who will be affected by these decisions?
- What data does it use?
- How will outputs be used?""",
            height=200
        )

        st.markdown("---")

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            evaluate_btn = st.button("🔍 Evaluate with AI", type="primary", use_container_width=True)

        with col2:
            clear_btn = st.button("🗑️ Clear Form", use_container_width=True)

        if clear_btn:
            st.session_state.evaluation_result = None
            st.session_state.use_case_data = None
            st.rerun()

        if evaluate_btn:
            # Validation
            if not name:
                st.error("Please enter a use case name")
            elif department == "Select...":
                st.error("Please select a department")
            elif not markets:
                st.error("Please select at least one target market")
            elif not data_types:
                st.error("Please select at least one data type")
            elif not description:
                st.error("Please enter a description")
            elif not api_key:
                st.error("Please enter your Groq API key in the sidebar")
            else:
                use_case_data = {
                    'name': name,
                    'department': department,
                    'ai_techniques': ai_techniques if ai_techniques != "Select..." else "Not specified",
                    'stage': stage if stage != "Select..." else "Not specified",
                    'markets': markets,
                    'data_types': data_types,
                    'description': description
                }

                with st.spinner("🔍 Analyzing use case against governance frameworks..."):
                    result = evaluate_use_case(use_case_data, api_key)

                    if result:
                        st.session_state.evaluation_result = result
                        st.session_state.use_case_data = use_case_data
                        st.success("✅ Evaluation complete! View results in the Results tab.")
                        st.balloons()

    with tab2:
        if st.session_state.evaluation_result and st.session_state.use_case_data:
            result = st.session_state.evaluation_result
            use_case = st.session_state.use_case_data

            # Overall Score Card
            st.markdown(f"""
            <div class="score-card">
                <div style="display: flex; justify-content: space-around; align-items: center;">
                    <div>
                        <div class="score-value">{result.get('overall_score', 'N/A')}</div>
                        <div class="score-label">Overall Score</div>
                    </div>
                    <div>
                        <div class="score-value" style="font-size: 2rem;">{result.get('risk_level', 'N/A')}</div>
                        <div class="score-label">Risk Level</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Executive Summary
            st.markdown("### 📋 Executive Summary")
            st.info(result.get('executive_summary', 'No summary available.'))

            # Risk Breakdown
            st.markdown("### ⚠️ Risk Assessment")

            risks = result.get('risks', {})

            col1, col2 = st.columns(2)

            risk_items = list(risks.items())

            for idx, (risk_name, risk_data) in enumerate(risk_items):
                with col1 if idx % 2 == 0 else col2:
                    risk_title = risk_name.replace('_', ' ').title()
                    level = risk_data.get('level', 'UNKNOWN')

                    icon = {'regulatory': '🏛️', 'bias': '⚖️', 'privacy': '🔒', 'transparency': '👁️'}.get(risk_name, '📊')

                    st.markdown(f"""
                    <div class="info-card">
                        <h4>{icon} {risk_title} Risk {get_risk_badge(level)}</h4>
                        <p>{risk_data.get('summary', 'No details available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Recommended Actions
            st.markdown("### ✅ Recommended Actions")

            actions = result.get('recommended_actions', [])

            if actions:
                for action in actions:
                    priority = action.get('priority', '-')
                    priority_color = {1: '🔴', 2: '🟠', 3: '🟡'}.get(priority, '⚪')

                    st.markdown(f"""
                    **{priority_color} P{priority}:** {action.get('action', 'N/A')}
                    *{action.get('regulation', '')}* → **Owner:** {action.get('owner', 'TBD')}
                    """)
            else:
                st.write("No specific actions recommended.")

            # Export Options
            st.markdown("---")
            st.markdown("### 📤 Export Report")

            col1, col2, col3 = st.columns(3)

            with col1:
                pdf_buffer = generate_pdf_report(use_case, result)
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"AIGovLens_Report_{use_case['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with col2:
                json_str = json.dumps({
                    'use_case': use_case,
                    'evaluation': result,
                    'generated_at': datetime.now().isoformat()
                }, indent=2)
                st.download_button(
                    label="📊 Download JSON",
                    data=json_str,
                    file_name=f"AIGovLens_Data_{use_case['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col3:
                if st.button("🔄 New Evaluation", use_container_width=True):
                    st.session_state.evaluation_result = None
                    st.session_state.use_case_data = None
                    st.rerun()

        else:
            st.info("👈 Enter a use case in the 'Evaluate Use Case' tab and click 'Evaluate with AI' to see results here.")


if __name__ == "__main__":
    main()
