
import streamlit as st
import os
from typing import Dict, List
from datetime import datetime
from streamlit.components.v1 import html

# >>> Hardcoded path to your attached image (already available)
IMAGE_PATH = "Playbook_framework_complete.png"
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
                "Seasoned **IT Business Analyst & Business Architect** with 15+ years of "
                "experience across finance, higher education, retail, and healthcare. "
                "**TOGAF 9.1** & **ITIL V3** certified; skilled at aligning business and IT via "
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


    def show_picture():
    st.title("Business Architecture Playbook: Visual Overview")
    col1, col2, col3 = st.columns([1, 20, 1])
    with col2:
        if os.path.exists(IMAGE_PATH):
            st.image(IMAGE_PATH, use_container_width=True)
        else:
            st.warning(f"Image not found at **{IMAGE_PATH}**.")
            
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

    st.sidebar.markdown("---")
    if st.sidebar.button("📁 Job Artefacts", use_container_width=True, key="nav_job_artefacts"):
        st.session_state.current_page = "artefacts_manager"
        st.session_state.current_artifact_id = None

def show_section_page(section_key: str):
    label = st.session_state.section_labels.get(section_key, section_key.title())
    st.title(label)

    # Content
    content_md = st.session_state.section_content.get(section_key, "_No content for this section yet._")
    st.markdown(content_md)

    # Artefacts for this section
    artefact_ids = st.session_state.artefacts_by_section.get(section_key, [])
    if artefact_ids:
        st.markdown("### Related Artefacts")
        for art_id in artefact_ids:
            art = st.session_state.artifacts.get(art_id)
            if not art:
                continue
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(f"**{art['name']}**  \n*Uploaded:* {art.get('created_at','')}")
            with col2:
                st.download_button(
                    label="Download",
                    data=art["bytes"],
                    file_name=art["name"],
                    mime=art["mime"],
                    key=f"dl_{art_id}",
                )
            with col3:
                if st.button("Open", key=f"open_{art_id}"):
                    st.session_state.current_page = "artifact"
                    st.session_state.current_artifact_id = art_id
                    st.rerun()

def show_artifact_page(artifact_id: str):
    art = st.session_state.artifacts.get(artifact_id)
    if not art:
        st.error("Artifact not found.")
        return
    section_key = art.get("section_key", "")
    section_label = st.session_state.section_labels.get(section_key, section_key)

    st.title(f"Artefact: {art['name']}")
    st.caption(f"Assigned to: {section_label} • Uploaded: {art.get('created_at','')}")
    st.download_button(
        "Download this artefact",
        data=art["bytes"],
        file_name=art["name"],
        mime=art["mime"],
        key=f"dl_single_{artifact_id}",
    )
    # For simplicity, we won't embed file previews for all types.
    st.info("Preview is not available for all file types. Use the download button to open the document.")

    if st.button(f"← Back to {section_label}"):
        st.session_state.current_page = "section"
        st.session_state.current_artifact_id = None
        st.session_state.current_section_key = section_key
        st.rerun()

def show_artefacts_manager():
    st.title("📁 Job Artefacts")
    st.write(
        "Upload documents (PDF, DOCX, etc.), then assign them to an existing resume section "
        "or create a new navigation section. Each artefact gets its **own page**."
    )
    with st.expander("Upload a new artefact", expanded=True):
        upload_col, assign_col = st.columns([2, 2])
        with upload_col:
            uploaded = st.file_uploader(
                "Choose a file",
                type=["pdf", "docx", "doc", "txt", "csv", "ppt", "pptx", "xlsx"],
                accept_multiple_files=False,
            )
        with assign_col:
            st.write("**Assign to:**")
            existing_labels = [st.session_state.section_labels[k] for k in st.session_state.section_order]
            assign_choice = st.radio(
                "Where should this artefact appear?",
                ["Existing section", "New navigation section"],
                horizontal=True,
            )
            target_key = None
            new_label = ""
            if assign_choice == "Existing section":
                label_to_key = {st.session_state.section_labels[k]: k for k in st.session_state.section_order}
                chosen_label = st.selectbox("Select section", options=existing_labels)
                target_key = label_to_key[chosen_label]
            else:
                new_label = st.text_input("New section label", placeholder="e.g., Certifications, Portfolio, Presentations")

            if st.button("Add Artefact"):
                if uploaded is None:
                    st.warning("Please upload a file first.")
                else:
                    if assign_choice == "Existing section":
                        art_id = add_artifact(uploaded, target_key)
                    else:
                        art_id = add_artifact(uploaded, "__NEW_SECTION__", new_section_label=new_label)

                    if art_id:
                        st.success("Artefact added successfully! It now appears under the chosen section.")
                        st.balloons()

    st.markdown("---")
    st.subheader("All Artefacts")
    # List all artefacts with navigation and download
    if not st.session_state.artifacts:
        st.caption("_No artefacts uploaded yet._")
    else:
        for art_id, meta in sorted(st.session_state.artifacts.items(), key=lambda x: x[1].get("created_at", "")):
            cols = st.columns([5, 2, 2, 2])
            with cols[0]:
                sec_label = st.session_state.section_labels.get(meta.get("section_key",""), "")
                st.write(f"**{meta['name']}**  \n*Section:* {sec_label}")
            with cols[1]:
                st.download_button(
                    "Download",
                    data=meta["bytes"],
                    file_name=meta["name"],
                    mime=meta["mime"],
                    key=f"dl_mgr_{art_id}",
                )
            with cols[2]:
                if st.button("Open Page", key=f"open_mgr_{art_id}"):
                    st.session_state.current_page = "artifact"
                    st.session_state.current_artifact_id = art_id
                    st.rerun()
            with cols[3]:
                # Optional: remove artefact
                if st.button("Remove", key=f"rm_{art_id}"):
                    # unlink from section
                    sec_key = meta.get("section_key","")
                    if sec_key in st.session_state.artefacts_by_section and art_id in st.session_state.artefacts_by_section[sec_key]:
                        st.session_state.artefacts_by_section[sec_key].remove(art_id)
                    # remove artefact
                    del st.session_state.artifacts[art_id]
                    st.toast("Artefact removed.", icon="🗑️")
                    st.experimental_rerun()

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
