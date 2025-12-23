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
st.set_page_config(
    page_title="Crochet Architect",
    page_icon="🧶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
    }
    .stExpander {
        background-color: #f0f8ff;
        border-radius: 8px;
    }
    .stInfo {
        background-color: #e8f4f8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE: STITCH LIBRARY WITH HYPERLINKS ---
STITCH_DATABASE = {
    "Treble Mesh": {
        "desc": "Creates a grid of open squares. Ideal for summer shawls and lacy garments.",
        "abbr_uk": "tr, ch1, sk1",
        "abbr_us": "dc, ch1, sk1",
        "video": "https://www.youtube.com/embed/9g0s3qTqj1g",
        "tutorial_name": "Filet Mesh Tutorial",
        "difficulty": "Beginner",
        "drape": "Airy"
    },
    "Granite Stitch": {
        "desc": "Also known as Moss Stitch. Dense, woven texture with excellent drape.",
        "abbr_uk": "dc, ch1, sk1",
        "abbr_us": "sc, ch1, sk1",
        "video": "https://www.youtube.com/embed/gUa6tLpZsio",
        "tutorial_name": "Moss Stitch Tutorial",
        "difficulty": "Beginner",
        "drape": "Structured"
    },
    "Double Crochet": {
        "desc": "Standard solid fabric. Fast to work up, versatile for most projects.",
        "abbr_uk": "tr",
        "abbr_us": "dc",
        "video": "https://www.youtube.com/embed/5wTgbdMs-bg",
        "tutorial_name": "Double Crochet Basics",
        "difficulty": "Beginner",
        "drape": "Medium"
    },
    "Granny Cluster": {
        "desc": "Classic 3-stitch groups. Used in traditional granny squares.",
        "abbr_uk": "3tr group",
        "abbr_us": "3dc group",
        "video": "https://www.youtube.com/embed/P_J_6r_L_pI",
        "tutorial_name": "Granny Cluster Tutorial",
        "difficulty": "Intermediate",
        "drape": "Medium"
    },
    "Shell Stitch": {
        "desc": "Creates beautiful fan-like shells. Great for edges and texture.",
        "abbr_uk": "5tr shell",
        "abbr_us": "5dc shell",
        "video": "https://www.youtube.com/embed/7lM8y2xPz-c",
        "tutorial_name": "Shell Stitch Guide",
        "difficulty": "Intermediate",
        "drape": "Airy"
    },
    "Popcorn Stitch": {
        "desc": "Dimensional bobbles. Perfect for textured amigurumi and toys.",
        "abbr_uk": "popcorn",
        "abbr_us": "popcorn",
        "video": "https://www.youtube.com/embed/1vKvqm76F-Q",
        "tutorial_name": "Popcorn Stitch Tutorial",
        "difficulty": "Advanced",
        "drape": "Dimensional"
    },
    "Linen Stitch": {
        "desc": "Creates a gridded, linen-like texture. Great for structured garments.",
        "abbr_uk": "dc, ch1",
        "abbr_us": "dc, ch1",
        "video": "https://www.youtube.com/embed/cCWnJEpwPLw",
        "tutorial_name": "Linen Stitch Guide",
        "difficulty": "Beginner",
        "drape": "Structured"
    },
    "Half Double Crochet": {
        "desc": "Medium height stitch. Versatile and works quickly.",
        "abbr_uk": "htr",
        "abbr_us": "hdc",
        "video": "https://www.youtube.com/embed/FGoTHr20xGE",
        "tutorial_name": "Half Double Crochet Basics",
        "difficulty": "Beginner",
        "drape": "Medium"
    }
}

# --- PRESET PATTERNS ---
PRESETS = {
    "Custom": {},
    "Classic Shawl": {
        "shape": "Square",
        "size": 100,
        "neck": 15,
        "stitch": "Treble Mesh",
        "description": "A flowing square shawl with neck opening."
    },
    "Baby Blanket": {
        "shape": "Rectangle",
        "size": 80,
        "neck": 0,
        "stitch": "Granite Stitch",
        "description": "A cozy rectangular blanket for babies."
    },
    "Coaster": {
        "shape": "Square",
        "size": 10,
        "neck": 0,
        "stitch": "Double Crochet",
        "description": "Quick little coaster in solid DC."
    },
    "Shawlette": {
        "shape": "Triangle",
        "size": 60,
        "neck": 0,
        "stitch": "Shell Stitch",
        "description": "Small triangular shawl with shell edge."
    }
}

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🧶 Crochet Architect")
st.sidebar.markdown("---")
st.sidebar.info(
    "**A tool to generate custom crochet patterns from parameters.**\n\n"
    "- Generate text patterns\n"
    "- Convert images to stitch charts\n"
    "- Learn stitch techniques\n\n"
    "[GitHub](https://github.com) | [About](#)"
)
st.sidebar.markdown("---")
measurement_system = st.sidebar.radio("Measurement System", ["Metric (cm)", "Imperial (inches)"])

# --- MAIN CONTENT TABS ---
tab1, tab2, tab3 = st.tabs(["📝 Pattern Generator", "🖼️ Image to Chart", "📚 Stitch Library"])

# ==========================================
# TAB 1: PATTERN GENERATOR
# ==========================================
with tab1:
    st.header("📝 Pattern Generator")
    st.markdown("Create custom crochet patterns with your specifications.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Configuration")
        
        # Preset Selector
        selected_preset = st.selectbox(
            "Load a Preset Pattern",
            list(PRESETS.keys()),
            help="Start with a template or choose 'Custom' for full control."
        )
        
        defaults = PRESETS[selected_preset]
        
        if selected_preset != "Custom":
            st.caption(f"_{PRESETS[selected_preset].get('description', '')}_")
        
        # Input Fields
        shape = st.selectbox(
            "Shape",
            ["Square", "Rectangle", "Circle", "Triangle"],
            index=0 if "shape" not in defaults else ["Square", "Rectangle", "Circle", "Triangle"].index(defaults.get("shape", "Square"))
        )
        
        unit = " inches" if "Imperial" in measurement_system else " cm"
        size = st.number_input(
            f"Final Size ({unit.strip()})",
            value=defaults.get("size", 100),
            min_value=5,
            step=5,
            help="Width of the final piece."
        )
        
        neck = st.number_input(
            f"Neck/Center Opening ({unit.strip()})",
            value=defaults.get("neck", 15),
            min_value=0,
            step=1,
            help="Leave at 0 for blankets/squares without opening."
        )
        
        colors = st.slider(
            "Number of Colors",
            min_value=1,
            max_value=12,
            value=6,
            help="How many colors to use in color stripes."
        )
        
        stitch_key = st.selectbox(
            "Stitch Type",
            list(STITCH_DATABASE.keys()),
            index=0 if "stitch" not in defaults else list(STITCH_DATABASE.keys()).index(defaults.get("stitch", "Double Crochet")),
            help="Choose the main stitch for your pattern."
        )
        
        # Display Stitch Info
        stitch_info = STITCH_DATABASE[stitch_key]
        st.info(
            f"**{stitch_key}** ({stitch_info['difficulty']})\n\n"
            f"{stitch_info['desc']}\n\n"
            f"**Drape:** {stitch_info['drape']}"
        )
        
        generate_btn = st.button("🎯 Generate Pattern", type="primary", use_container_width=True)
    
    # Pattern Output
    with col2:
        if generate_btn:
            st.session_state['generated_pattern'] = True
            
            with st.spinner("Generating your pattern..."):
                # Calculate pattern metrics
                unit_abbr = '"' if "Imperial" in measurement_system else "cm"
                size_per_color = int(size / colors) if colors > 0 else size
                est_rounds = int((size - neck) / 2.5) if neck > 0 else int(size / 2.5)
                
                # Build Pattern Text
                pattern_text = f"""# {shape} {stitch_key} Pattern

## Project Summary
- **Shape:** {shape}
- **Final Dimensions:** {size}{unit_abbr} width
- **Neck/Opening:** {neck}{unit_abbr} (if applicable)
- **Stitch:** {stitch_key}
- **Colors:** {colors}

## Stitch Information
**Abbreviation (UK):** `{stitch_info['abbr_uk']}`
**Abbreviation (US):** `{stitch_info['abbr_us']}`
**Difficulty Level:** {stitch_info['difficulty']}
**Drape Type:** {stitch_info['drape']}

## Key Abbreviations
| Abbreviation | Meaning |
|---|---|
| ch | Chain |
| st/sts | Stitch/Stitches |
| sc | Single Crochet |
| dc | Double Crochet |
| tr | Treble |
| sk | Skip |
| sl st | Slip Stitch |
| inc | Increase |
| dec | Decrease |

## Pattern Instructions

### Foundation
1. **Starting Chain:** Create a foundation chain of approximately {int(neck * 1.5 if neck > 0 else size * 0.5)}{unit_abbr}
2. **Join:** Slip stitch to form a ring (or work flat if rectangular)
3. **Setup Round:** Work {stitch_key} stitches evenly around the ring

### Body (Work in Rounds)
- **Rounds 1-{est_rounds}:** Continue working {stitch_key} in rounds
- **Increases:** Place increases at {4 if shape == "Square" else 3} evenly spaced points per round (for even expansion)
- **Row Height:** Approximately 2-3{unit_abbr} per round (adjust based on your gauge)

### Color Pattern
Work the following colors in striped rounds:
"""
                for i in range(colors):
                    pattern_text += f"\n- **Color {i+1}:** Rounds {i*size_per_color//2}-{(i+1)*size_per_color//2}"
                
                pattern_text += f"""

### Finishing
1. Cut yarn leaving 6{unit_abbr} tail
2. Pull through last loop
3. Weave in all ends
4. **Block:** Wet block and pin to shape for best results

## Gauge & Notes
- Adjust hook size if your gauge is off
- This pattern is a guideline—modify to fit your yarn weight
- Always swatch first!

---
**[Watch {stitch_info['tutorial_name']} →]({stitch_info['video'].replace('/embed/', '/watch?v=')})**
"""
                
                st.session_state['pattern_content'] = pattern_text
        
        # Display Generated Pattern
        if 'generated_pattern' in st.session_state and st.session_state['generated_pattern']:
            st.markdown(st.session_state['pattern_content'])
            
            # Download Button
            col_down1, col_down2 = st.columns(2)
            with col_down1:
                st.download_button(
                    label="📥 Download as Text",
                    data=st.session_state['pattern_content'],
                    file_name=f"crochet_pattern_{shape.lower()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_down2:
                st.download_button(
                    label="📥 Download as Markdown",
                    data=st.session_state['pattern_content'],
                    file_name=f"crochet_pattern_{shape.lower()}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            # Video Tutorial
            st.markdown("---")
            st.subheader(f"🎥 Learn {stitch_key}")
            st.video(stitch_info['video'].replace('/embed/', '/watch?v='))

# ==========================================
# TAB 2: IMAGE TO CHART
# ==========================================
with tab2:
    st.header("🖼️ Image to Crochet Chart")
    st.markdown("Convert images to pixel-based crochet charts (ideal for C2C, Filet, or Tapestry crochet).")
    
    uploaded_file = st.file_uploader(
        "Upload an image (JPEG, PNG, or GIF)",
        type=['jpg', 'jpeg', 'png', 'gif'],
        help="Upload a small, simple image for best results."
    )
    
    if uploaded_file is not None:
        # Load and display original
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
        
        # Settings
        st.subheader("⚙️ Chart Settings")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            width_sts = st.slider(
                "Width (stitches/blocks)",
                min_value=10,
                max_value=100,
                value=30,
                help="Wider = more detail, but more stitches to count."
            )
        
        with col_s2:
            num_colors = st.slider(
                "Number of Colors",
                min_value=2,
                max_value=20,
                value=6,
                help="Reduce image to N distinct colors."
            )
        
        # Convert Button
        if st.button("🔄 Convert to Chart", type="primary", use_container_width=True):
            with st.spinner("Converting image to stitch chart..."):
                try:
                    # Resize maintaining aspect ratio
                    w_percent = (width_sts / float(image.size[0]))
                    h_size = int((float(image.size[1]) * float(w_percent)))
                    
                    # Resize with NEAREST for pixel art effect
                    img_small = image.resize((width_sts, h_size), Image.Resampling.NEAREST)
                    
                    # Quantize to N colors
                    img_quantized = img_small.quantize(colors=num_colors)
                    
                    # Store in session
                    st.session_state['chart_grid'] = np.array(img_quantized)
                    st.session_state['chart_image'] = img_quantized
                    st.session_state['chart_dimensions'] = (width_sts, h_size)
                    
                except Exception as e:
                    st.error(f"Error converting image: {e}")
        
        # Display Chart
        if 'chart_image' in st.session_state:
            with col2:
                st.subheader("Chart Preview")
                # Resize for display
                display_img = st.session_state['chart_image'].resize(
                    (500, 500),
                    Image.Resampling.NEAREST
                )
                st.image(display_img, use_container_width=True)
            
            # Chart Info & Export
            st.markdown("---")
            width, height = st.session_state['chart_dimensions']
            st.success(f"✅ Chart Generated: **{width}W × {height}H stitches**")
            
            # Color Palette
            st.subheader("Color Palette")
            palette = st.session_state['chart_image'].getpalette()
            num_colors_actual = len(palette) // 3
            
            cols = st.columns(min(num_colors_actual, 6))
            for idx in range(num_colors_actual):
                rgb = tuple(palette[idx*3:idx*3+3])
                with cols[idx % len(cols)]:
                    st.color_picker(f"Color {idx+1}", f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}", disabled=True)
            
            # Download Chart
            st.subheader("Export Chart")
            col_e1, col_e2, col_e3 = st.columns(3)
            
            with col_e1:
                # Save as image
                buf = io.BytesIO()
                st.session_state['chart_image'].save(buf, format="PNG")
                st.download_button(
                    label="📥 Chart (PNG)",
                    data=buf.getvalue(),
                    file_name="crochet_chart.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            with col_e2:
                # Export as CSV (for counting)
                csv_data = "Row,Stitch Count,Colors\n"
                grid = st.session_state['chart_grid']
                for row_idx, row in enumerate(grid):
                    color_counts = np.bincount(row)
                    csv_data += f"{row_idx},{len(row)},{len(color_counts)}\n"
                
                st.download_button(
                    label="📥 Data (CSV)",
                    data=csv_data,
                    file_name="crochet_chart_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_e3:
                st.info("💡 Tip: Use C2C (Corner-to-Corner) or Filet Crochet for chart patterns.")

# ==========================================
# TAB 3: STITCH LIBRARY
# ==========================================
with tab3:
    st.header("📚 Stitch Reference Library")
    st.markdown("Learn all available stitches with detailed descriptions and video tutorials.")
    
    # Filter options
    col_filt1, col_filt2 = st.columns(2)
    with col_filt1:
        difficulty_filter = st.multiselect(
            "Filter by Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            default=["Beginner", "Intermediate", "Advanced"]
        )
    with col_filt2:
        drape_filter = st.multiselect(
            "Filter by Drape",
            ["Airy", "Medium", "Structured", "Dimensional"],
            default=["Airy", "Medium", "Structured", "Dimensional"]
        )
    
    st.markdown("---")
    
    # Display filtered stitches
    for name, info in STITCH_DATABASE.items():
        # Apply filters
        if info['difficulty'] not in difficulty_filter or info['drape'] not in drape_filter:
            continue
        
        with st.expander(f"🧶 **{name}** — {info['difficulty']} | {info['drape']}"):
            col_exp1, col_exp2 = st.columns([2, 1])
            
            with col_exp1:
                st.markdown(f"**Description:** {info['desc']}")
                
                # Abbreviations
                st.markdown("**Abbreviations:**")
                abbr_col1, abbr_col2 = st.columns(2)
                with abbr_col1:
                    st.code(f"UK: {info['abbr_uk']}", language="text")
                with abbr_col2:
                    st.code(f"US: {info['abbr_us']}", language="text")
                
                st.markdown(f"[🎥 Watch Tutorial: {info['tutorial_name']}](https://www.youtube.com/watch?v={info['video'].split('v=')[-1]})")
            
            with col_exp2:
                st.metric("Difficulty", info['difficulty'])
                st.metric("Drape", info['drape'])
            
            # Embedded video
            st.markdown("---")
            with st.expander("📺 Video Tutorial"):
                st.video(info['video'].replace('/embed/', '/watch?v='))
    
    # Summary statistics
    st.markdown("---")
    st.subheader("Library Statistics")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Stitches", len(STITCH_DATABASE))
    with col_stat2:
        beginner_count = sum(1 for s in STITCH_DATABASE.values() if s['difficulty'] == 'Beginner')
        st.metric("Beginner Stitches", beginner_count)
    with col_stat3:
        advanced_count = sum(1 for s in STITCH_DATABASE.values() if s['difficulty'] == 'Advanced')
        st.metric("Advanced Stitches", advanced_count)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "<p>🧶 Crochet Architect v1.0</p>"
    "<p>Made with ❤️ for fiber artists</p>"
    "<p><a href='https://github.com'>GitHub</a> | <a href='#'>Documentation</a></p>"
    "</div>",
    unsafe_allow_html=True
)
