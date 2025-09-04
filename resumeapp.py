
import streamlit as st
import os
from typing import Dict, List
from datetime import datetime

# =============================
# App Configuration
# =============================
st.set_page_config(
    page_title="Interactive Resume & Job Artefacts",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# Helpers & Initialization
# =============================
def slugify(label: str) -> str:
    """Create a safe key for sections based on label."""
    return (
        label.strip().lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("&", "and")
        .replace("__", "_")
    )

def init_state():
    if "section_order" not in st.session_state:
        # Default resume sections (keys)
        st.session_state.section_order = [
            "summary",
            "skills",
            "competencies",
            "experience",
            "adaptability",
            "services",
        ]
    if "section_labels" not in st.session_state:
        st.session_state.section_labels: Dict[str, str] = {
            "summary": "Professional Summary",
            "skills": "Skills",
            "competencies": "Core Competencies",
            "experience": "Professional Experience",
            "adaptability": "Adaptability to Emerging Trends",
            "services": "Business Arcitecture and Business Analysis Services",
        }
    if "section_content" not in st.session_state:
        # Summary-only content for each section (derived from the user's resume)
        st.session_state.section_content: Dict[str, str] = {
            "summary": (
                "- Seasoned **IT Business Analyst & Business Architect** with 15+ years of experience across finance, higher education, retail, and healthcare\n"
                "- **TOGAF 9.1** & **ITIL V3** certified; skilled at aligning business and IT via "
                "capability-based planning, process improvement, and Agile delivery."
            ),
            "skills": (
                "- **Strategic & Leadership:** Enterprise Architecture (TOGAF), Business Capability Planning, Roadmaps, Business–IT Alignment, Team Leadership\n"
                "- **Business Analysis:** Elicitation & Documentation (BRD, user stories, use cases), BPMN/CMMN/UML, Process Improvement, UAT Leadership, Solution Evaluation\n"
                "- **Technical:** Identity & Access Management (IAM), SaaS/COTS configuration, SQL & data analysis, Systems Integration, ITSM (ITIL)\n"
                "- **Tools & Methods:** Agile (Scrum/Kanban) & Waterfall, **Sparx EA**, **LeanIX**, **Jira**, **ServiceNow**, **Confluence**, **SharePoint**"
            ),
            "competencies": (
                "- **Business Architecture & Analysis:** Capability/Information/Org mapping, strategic roadmaps, target operating models\n"
                "- **Requirements & Design:** BABOK-aligned analysis, solution design definition, traceability\n"
                "- **Solution Assessment & Validation:** Fit-gap, COTS/SaaS configuration, test strategy & UAT\n"
                "- **Stakeholder Engagement:** Workshops/JAD, cross-functional facilitation, clear communication to executives\n"
                "- **Agile Delivery & Improvement:** Iterative delivery, continuous improvement, change enablement"
            ),
            "experience": (
                "**Highlights:**\n"
                "- Led cloud **legal case management** implementation and UAT at **WorkSafeBC**.\n"
                "- At **UBC**, built capability maps, value streams, and target-state roadmaps; defined last‑mile integrations for **Workday**.\n"
                "- At **ICBC**, introduced **Business Capability Planning**; reduced document management TCO by ~55% (from $1.6M to $0.7M); delivered **Oracle IAM** integration.\n"
                "- At **Safeway**, established **ITAM/SAM** practice; integrated HPAM, CMDB, Remedy, LDAP, Lawson; implemented Sun **IAM**, CA **ESP** scheduling, and Symantec Endpoint."
            ),
            "adaptability": (
                "Continuously aligns BA practice with **emerging trends**: enterprise cloud, SaaS, "
                "data-driven decisioning, automation, and architecture‑led transformation. "
                "Active in IIBA/BizArch communities; rapidly adopts new tools & methods to drive measurable outcomes."
            ),
           "services": (
                "**Business Architecture Services:**\n"
                "- Developed comprehensive business architecture frameworks, including motivation models, governance models, and strategic roadmaps for organizations like Capilano University, BC Housing, and UBC, facilitating successful enterprise architecture practices and IT/business alignment.\n\n"
                "**- Competency in:**\n"
                "- Capability, Information & Organization Mapping\n"
                "- Motivation, Benefits, As-Is and To-Be Target Operating Models\n"
                "- Process Hierarchy Models\n"
                "- Value Streams\n"
                "- Strategic Roadmaps\n"
                "- Business / IT Alignment maps\n"
                "- Vision, Strategy, Objectives, and Measures Mapping\n"
                "\n\n"
                "**Business Analysis Services:**\n"
                "- Led requirement gathering, analysis, and documentation efforts across various projects, including CRM upgrades at Vancity, case management solutions at WorksafeBC, and enterprise system implementations at UBC. Notable for crafting detailed business cases, process maps, and user stories to guide project execution. \n\n"
                "**- Competency in:**\n"
                "- Current state analysis and future state analysis documents \n"
                "- Requirements Definition Document \n"
                "- Epic, Feature and Stories\n"
                "- Data Definition Requirements Document\n"
                "- Gap Analysis Document \n"
                "- Assistance with UAT Document\n" 
                "- Business Process Maps\n"   
                "- System deployment documents (i.e., deployment plan, service desk guide, etc.)\n" 
                "- Progress status reports\n" 
                "- Business cases\n" 
                "- Resource Estimations\n" 
            ),
        }
            
    if "artefacts_by_section" not in st.session_state:
        # Mapping: section_key -> List[artifact_id]
        st.session_state.artefacts_by_section: Dict[str, List[str]] = {k: [] for k in st.session_state.section_order}
    if "artifacts" not in st.session_state:
        # Mapping: artifact_id -> dict with metadata and bytes
        st.session_state.artifacts: Dict[str, dict] = {}
    if "current_page" not in st.session_state:
        # "section", "artifact", or "artefacts_manager"
        st.session_state.current_page = "section"
    if "current_section_key" not in st.session_state:
        st.session_state.current_section_key = "summary"
    if "current_artifact_id" not in st.session_state:
        st.session_state.current_artifact_id = None

def add_custom_section(label: str) -> str:
    key = slugify(label)
    # Ensure uniqueness
    base = key
    i = 2
    while key in st.session_state.section_labels:
        key = f"{base}_{i}"
        i += 1
    st.session_state.section_labels[key] = label
    st.session_state.section_order.append(key)
    st.session_state.section_content[key] = f"Custom section **{label}**. Upload and attach artefacts here from the Job Artefacts page."
    st.session_state.artefacts_by_section[key] = []
    return key

def add_artifact(file, assign_to: str, new_section_label: str = ""):
    """Store the uploaded file in session state and link to a section."""
    if file is None:
        st.warning("Please upload a file first.")
        return None

    # Create artifact id
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    artifact_id = f"artifact_{timestamp}"

    # Read bytes
    data = file.read()
    name = file.name
    mime = file.type or "application/octet-stream"

    # If creating a brand-new section
    target_section_key = assign_to
    if assign_to == "__NEW_SECTION__":
        if not new_section_label.strip():
            st.error("Please provide a label for the new navigation section.")
            return None
        target_section_key = add_custom_section(new_section_label.strip())

    # Save artifact
    st.session_state.artifacts[artifact_id] = {
        "name": name,
        "mime": mime,
        "bytes": data,
        "section_key": target_section_key,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    # Link artifact to section
    if target_section_key not in st.session_state.artefacts_by_section:
        st.session_state.artefacts_by_section[target_section_key] = []
    st.session_state.artefacts_by_section[target_section_key].append(artifact_id)

    return artifact_id

# =============================
# Rendering Functions
# =============================
def render_sidebar():
    st.sidebar.title("Resume Navigator")
    st.sidebar.caption("Use the buttons below to open each section.")
    # Navigation buttons for each section (in order)
    for key in st.session_state.section_order:
        label = st.session_state.section_labels.get(key, key.title())
        if st.sidebar.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.current_page = "section"
            st.session_state.current_section_key = key
            
def show_section_page(section_key: str):
    label = st.session_state.section_labels.get(section_key, section_key.title())
    st.title(label)

        # Show the infographic image on the Core Competencies page
    if section_key == "competencies":
        img_path = "Infograph.jpg"   # uploaded image path
        if os.path.exists(img_path):
            st.markdown("###")
            st.image(img_path, use_container_width=True)
            
        else:
            st.info(
                "The infographic image was not found at `Infograph.jpg`."
                " Please place it there to display it here."
            )


    # Content
    content_md = st.session_state.section_content.get(section_key, "_No content for this section yet._")
    st.markdown(content_md)


# =============================
# Main
# =============================
def main():
    init_state()
    render_sidebar()

    if st.session_state.current_page == "artefacts_manager":
        show_artefacts_manager()
    elif st.session_state.current_page == "artifact" and st.session_state.current_artifact_id:
        show_artifact_page(st.session_state.current_artifact_id)
    else:
        # Default to section page
        if st.session_state.current_section_key not in st.session_state.section_labels:
            st.session_state.current_section_key = "summary"
        show_section_page(st.session_state.current_section_key)

if __name__ == "__main__":
    main()
