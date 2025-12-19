# Crochet Architect

A web-based tool for generating custom crochet patterns, converting images to stitch charts, and learning crochet stitches with embedded video tutorials.

## Features

✨ **Pattern Generator** – Create custom crochet patterns based on shape, size, stitch type, color count, and more
🖼️ **Image to Chart** – Convert JPEG/PNG images to pixel-based crochet charts (C2C, Filet, Tapestry)
📚 **Stitch Library** – Browse 8+ crochet stitches with abbreviations (UK/US) and embedded YouTube tutorials
📥 **Download Options** – Export patterns as text, markdown, or PNG charts

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/crochet-architect.git
   cd crochet-architect
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deploying to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free)

### Deployment Steps

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://share.streamlit.io)**

3. **Click "New app"** and select:
   - Repository: `yourusername/crochet-architect`
   - Branch: `main`
   - Main file path: `app.py`

4. **Click "Deploy"** – Streamlit Cloud will automatically install dependencies from `requirements.txt`

5. **Share your link!** Your app is now live at `https://share.streamlit.io/yourusername/crochet-architect/main/app.py`

## File Structure

```
crochet-architect/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── LICENSE               # License information
```

## Usage

### Pattern Generator
1. Select a preset or choose "Custom"
2. Set your shape, size, opening, colors, and stitch
3. Click "Generate Pattern"
4. Download as TXT or Markdown
5. Watch the embedded video tutorial for the chosen stitch

### Image to Chart
1. Upload a JPEG, PNG, or GIF
2. Set chart width (stitches) and number of colors
3. Click "Convert to Chart"
4. Download as PNG or CSV
5. Use with C2C, Filet, or Tapestry crochet

### Stitch Library
- Browse all available stitches
- Filter by difficulty or drape type
- View UK/US abbreviations
- Watch video tutorials directly in the app

## Customization

### Adding New Stitches

Edit the `STITCH_DATABASE` dictionary in `app.py`:

```python
"My New Stitch": {
    "desc": "Description of the stitch",
    "abbr_uk": "abbreviation (UK)",
    "abbr_us": "abbreviation (US)",
    "video": "https://www.youtube.com/embed/VIDEO_ID",
    "tutorial_name": "Stitch Name Tutorial",
    "difficulty": "Beginner",  # or "Intermediate", "Advanced"
    "drape": "Airy"  # or "Medium", "Structured", "Dimensional"
}
```

### Adding New Presets

Edit the `PRESETS` dictionary in `app.py`:

```python
"Preset Name": {
    "shape": "Square",
    "size": 100,
    "neck": 15,
    "stitch": "Treble Mesh",
    "description": "A description of this preset"
}
```

## Requirements

See `requirements.txt` for full dependencies:

- **streamlit** – Web app framework
- **pillow** – Image processing
- **numpy** – Numerical computing

## Troubleshooting

**Issue:** Image conversion fails
- **Solution:** Ensure image is under 10MB and in JPG/PNG/GIF format

**Issue:** Videos not loading in Streamlit Cloud
- **Solution:** This is normal. Videos may take a moment to load. Refresh the page.

**Issue:** App loads slowly
- **Solution:** Clear your browser cache and reload, or use incognito mode

## Contributing

Contributions welcome! To add features:

1. Fork the repository
2. Create a branch (`git checkout -b feature/my-feature`)
3. Make changes and test locally
4. Commit changes (`git commit -m "Add feature"`)
5. Push to your fork (`git push origin feature/my-feature`)
6. Open a Pull Request

## Roadmap

- [ ] Gauge calculator (stitches/rows per inch)
- [ ] Yarn weight selector
- [ ] Metric/Imperial toggle (DONE ✓)
- [ ] PDF export for patterns
- [ ] Color palette import from image
- [ ] Granny square calculator
- [ ] Amigurumi sizing guide
- [ ] Mobile app version

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues, questions, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/yourusername/crochet-architect/issues)
- Email: your.email@example.com

## Credits

- Stitch tutorials from [Crochet Crowd](https://thecrochetcrowd.com)
- Image quantization via Python [Pillow](https://python-pillow.org/)
- Built with [Streamlit](https://streamlit.io/)

---

**Made with ❤️ by fiber artists, for fiber artists.**

Happy crocheting! 🧶

Update

### **Key Improvements**

1.  **Beginner Mode Toggle:** In the sidebar, you can now select "Beginner". This fundamentally changes how the pattern instructions are displayed.[1]
2.  **Interactive Explainers:** Instead of a dense block of text, Beginner Mode uses `st.expander` elements. Each core step of the pattern is a clickable header that reveals a simple explanation and a video tutorial for that specific concept.[2][3]
3.  **New Glossary:** I've created a `GLOSSARY` at the top of the code. This contains simple, clear definitions for terms like "Foundation Chain", "Form a Ring", "Setup Round", and "Gauge". It's easy for you to add more terms to this dictionary in the future.[4][5][6][7]
4.  **Context-Aware Instructions:** The tool now correctly differentiates between projects that are worked flat (like a blanket) and those worked in a ring (like a coaster), providing the right instructions for each.[8]

Now, when you select "Coaster" and "Beginner," the instructions will be broken down into easy, digestible tutorials, making the process much more approachable for you and your family.
