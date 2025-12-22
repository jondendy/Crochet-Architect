import streamlit as st
import numpy as np
from PIL import Image
import io

import streamlit as st
import hmac

# --- PASSWORD PROTECTION ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password has already been validated
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.text_input(
        "Please enter your password to access Crochet Architect:", 
        type="password", 
        on_change=password_entered, 
        key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not run any more of the app

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Crochet Architect", page_icon="🧶", layout="wide")

# --- GLOSSARY FOR BEGINNERS ---
# This new dictionary holds the explanations for beginner mode.
GLOSSARY = {
    "foundation_chain": {
        "term": "Foundation Chain",
        "explanation": "This is the very first row of chains you make. It's the 'foundation' that the rest of your project is built upon. Each stitch in the next row will be worked into one of these chain links.",
        "video": "https://www.youtube.com/watch?v=O8ZQNvY-9FY"
    },
    "form_a_ring": {
        "term": "Form a Ring",
        "explanation": "To create a circular starting point (for a coaster, hat, or granny square), you join the two ends of your foundation chain. You do this by inserting your hook into the very first chain you made and making a 'slip stitch' to connect them, forming a loop.",
        "video": "https://www.youtube.com/watch?v=Z7M133vWziI"
    },
    "work_flat": {
        "term": "Work Flat",
        "explanation": "This means you are creating a rectangular or flat piece, like a scarf or blanket. At the end of each row, you will turn your entire project around to start crocheting back in the other direction.",
        "video": "https://www.youtube.com/watch?v=F3H9nBq6J1A"
    },
    "setup_round": {
        "term": "Setup Round / Row",
        "explanation": "This is the first round or row of actual stitches (like Double Crochet) that you work into your foundation. This round 'sets up' the pattern and establishes the stitch count that you will build upon in the next rounds.",
        "video": "https://www.youtube.com/watch?v=L5oG_y3u2pU"
    },
    "gauge": {
        "term": "Gauge (Tension Square)",
        "explanation": "Gauge is the measurement of how many stitches and rows fit into a 10cm x 10cm square. It's crucial for making sure your project ends up the right size. Before starting, you should always make a small test square (a 'swatch') to see if your tension matches the pattern's gauge.",
        "video": "https://www.youtube.com/watch?v=9_tHOr2-A7I"
    }
}

# --- STITCH & PRESET DATABASES (from previous version) ---
STITCH_DATABASE = {
    "Treble Mesh": {\"desc\": \"Creates a grid of open squares.\", \"abbr_uk\": \"tr, ch1, sk1\", \"abbr_us\": \"dc, ch1, sk1\", \"video\": \"https://www.youtube.com/embed/9g0s3qTqj1g\"},
    "Granite Stitch": {\"desc\": \"Also known as Moss Stitch. Dense, woven texture.\", \"abbr_uk\": \"dc, ch1, sk1\", \"abbr_us\": \"sc, ch1, sk1\", \"video\": \"https://www.youtube.com/embed/gUa6tLpZsio\"},
    "Double Crochet": {\"desc\": \"Standard solid fabric.\", \"abbr_uk\": \"tr\", \"abbr_us\": \"dc\", \"video\": \"https://www.youtube.com/embed/5wTgbdMs-bg\"},
    "Granny Cluster": {\"desc\": \"Classic 3-stitch groups.\", \"abbr_uk\": \"3tr group\", \"abbr_us\": \"3dc group\", \"video\": \"https://www.youtube.com/embed/P_J_6r_L_pI\"}
    }
    PRESETS = {
    "Custom": {},
        "Classic Shawl": {\"shape\": \"Square\", \"size\": 100, \"neck\": 15, \"stitch\": \"Treble Mesh\"},
        "Baby Blanket": {\"shape\": \"Rectangle\", \"size\": 80, \"neck\": 0, \"stitch\": \"Granite Stitch\"},
        "Coaster": {\"shape\": \"Circle\", \"size\": 10, \"neck\": 0, \"stitch\": \"Granny Cluster\"}
        }
                         
# --- SIDEBAR ---
st.sidebar.title("🧶 Crochet Architect")
st.sidebar.markdown("---")
# NEW: Experience Level Toggle
experience_level = st.sidebar.radio(
    "Experience Level",
    ["Experienced", "Beginner"],
    help="'Beginner' mode will add detailed explanations for core crochet terms within the pattern."
    
st.sidebar.markdown("---")
measurement_system = st.sidebar.radio("Measurement System", ["Metric (cm)", "Imperial (inches)"])
                  
# --- MAIN UI TABS ---
st.title("🧶 Crochet Architect")
tab1, tab2, tab3 = st.tabs(["📝 Pattern Generator", "🖼️ Image to Chart", "📚 Stitch Library"])
                  
with tab1:
# --- Inputs remain the same ---
    col1, col2 = st.columns([1, 2])
    with col1:
    st.subheader("⚙️ Configuration")
    selected_preset = st.selectbox("Load a Preset", list(PRESETS.keys()))
    defaults = PRESETS[selected_preset]
    shape = st.selectbox("Shape", ["Square", "Rectangle", "Circle", "Triangle"], index=["Square", "Rectangle", "Circle", "Triangle"].index(defaults.get("shape", "Square")) if "shape" in defaults else 0)
         unit = \"in\" if \"Imperial\" in measurement_system else \"cm\"
         size = st.number_input(f"Final Size ({unit})", value=defaults.get("size", 100))
             neck = st.number_input(f"Neck/Center Opening ({unit})", value=defaults.get("neck", 0))
                 stitch_key = st.selectbox("Stitch Type", list(STITCH_DATABASE.keys()), index=list(STITCH_DATABASE.keys()).index(defaults.get("stitch", "Double Crochet")) if "stitch" in defaults else 0)
                           generate_btn = st.button("🎯 Generate Pattern", type="primary", use_container_width=True)
                                       
# --- NEW: Dynamic Pattern Rendering ---
    with col2:
        if generate_btn:
            st.subheader("Your Custom Pattern")
                s_info = STITCH_DATABASE[stitch_key]
                      is_flat = shape in [\"Rectangle\", \"Triangle\"]
                      has_opening = neck > 0
                             
# --- BEGINNER MODE RENDERER ---
if experience_level == 'Beginner':
st.info(\"You're in Beginner Mode! Click on any step to learn more about it.\")\n\n                with st.expander("Understanding Gauge (IMPORTANT!)", expanded=False):\n                    st.markdown(GLOSSARY['gauge']['explanation'])\n                    st.video(GLOSSARY['gauge']['video'])\n                \n                st.markdown(\"### Foundation\")\n                with st.expander("Step 1: Foundation Chain", expanded=True):\n                    st.markdown(f\"**Action:** Create a **Foundation Chain** of approximately **{neck if has_opening else size//2}{unit}**.\")\n                    st.markdown(f\"---\n**What is a 'Foundation Chain'?**\n{GLOSSARY['foundation_chain']['explanation']}")\n                    st.video(GLOSSARY['foundation_chain']['video'])\n                \n                if not is_flat:\n                    with st.expander("Step 2: Form a Ring", expanded=True):\n                        st.markdown(\"**Action:** Join the chain with a slip stitch to **Form a Ring**.\")\n                        st.markdown(f\"---\n**What does 'Form a Ring' mean?**\n{GLOSSARY['form_a_ring']['explanation']}")\n                        st.video(GLOSSARY['form_a_ring']['video'])\n                else:\n                     with st.expander("Step 2: Work Flat", expanded=True):\n                        st.markdown(\"**Action:** Do not join the chain. You will **Work Flat**.\")\n                        st.markdown(f\"---\n**What does 'Work Flat' mean?**\n{GLOSSARY['work_flat']['explanation']}")\n                        st.video(GLOSSARY['work_flat']['video'])\n\n                st.markdown(\"### Body of the Project\")\n                with st.expander("Step 3: Setup Round/Row", expanded=True):\n                    st.markdown(f\"**Action:** Work your first row of **{stitch_key}** stitches into the foundation.\")\n                    st.markdown(f\"---\n**What is a 'Setup Round'?**\n{GLOSSARY['setup_round']['explanation']}")\n                    st.video(GLOSSARY['setup_round']['video'])\n\n                with st.expander("Step 4: Continue the Pattern", expanded=True):\n                    st.markdown(f\"**Action:** Continue working new rows/rounds of **{stitch_key}**.\")\n                    st.markdown(f\"- **If working in a ring:** Make sure to add increases evenly to keep it from curling.\n- **If working flat:** Remember to chain 1 and turn your work at the end of each row.\")\n                    st.markdown(\"Continue until the project reaches the desired size of **{size}{unit}**.\")\n                    st.markdown(f\"**Learn the main stitch:**\")\n                    st.video(s_info['video'].replace(\"/embed/\", \"/watch?v=\"))\n\n            # --- EXPERIENCED MODE RENDERER ---\n            else:\n                st.success(\"Experienced Mode: Pattern generated below.\")\n                pattern_text = f\"\"\"\n                ### Foundation\n                1.  **Starting Chain:** Create a foundation chain of approx. **{neck if has_opening else size//2}{unit}**.\n                2.  **Join:** {'Slip stitch to form a ring.' if not is_flat else 'Prepare to work flat.'}\n                \n                ### Body\n                3.  **Setup Round:** Work the first round/row of **{stitch_key}** stitches.\n                4.  **Increases:** {'Place increases at corners to keep the piece flat.' if not is_flat else 'Chain 1 and turn at the end of each row.'}\n                5.  **Continue:** Work until the piece measures **{size}{unit}**.\n\n                ---\n                #### Stitch Key:\n                - **Main Stitch:** {stitch_key} (`{s_info['abbr_us']}`)\n                - [Watch Tutorial]({s_info['video'].replace('/embed/', '/watch?v=')})\n                \"\"\"\n                st.markdown(pattern_text)\n\n# The other tabs (Image to Chart, Stitch Library) remain unchanged.\n# You can copy and paste the code from the previous version for them.\nwith tab2:\n    st.header(\"🖼️ Image to Crochet Chart\")\n    #...(paste previous code here)\n\nwith tab3:\n    st.header(\"📚 Stitch Reference Library\")\n    #...(paste previous code here)\n```

