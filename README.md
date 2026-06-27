# 🇮🇸 macOS Icelandic Monolingual Dictionary Builder

Bring seamless, system-wide Icelandic definitions to your Mac! 

This repository provides an automated build pipeline that pairs modern Icelandic definitions from **Íslensk nútímamálsorðabók (ÍNO)** with the **BÍN** inflection database. Once compiled, you can use macOS's native **Force Click / Three-Finger Tap** "Look Up" feature on *any* heavily inflected Icelandic word (like *gleraugunum*, *viðskiptanna*, or *borðuðu*) inside Safari, Pages, or Mail and instantly see its base dictionary entry.

---

## ⚖️ Why This is a "Builder" (License Note)

The underlying definition data provided by Árnastofnun is licensed under **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**. 

Because the "NoDerivatives" (ND) clause strictly forbids the distribution of modified or converted versions of the data, **pre-compiled `.dictionary` files cannot legally be hosted here for download.** Instead, this project is an automated, open-source tool allowing you to compile the dictionary privately on your own Mac for your personal use.

---

## 🛠️ Prerequisites

Before building, ensure you have gathered your developer tools and asset files:

1. **Xcode Command Line Tools**: Open your Terminal and run:
   ```bash
   xcode-select --install
   ```
2. **Apple Dictionary Development Kit**: Download the **Additional Tools for Xcode** package from the Apple Developer portal. 
3. **Source Dictionary Data**: Download the official XML export file of the *Íslensk nútímamálsorðabók* from Árnastofnun. Create a folder named `data` in this project's root and save the file inside exactly as:
   ```text
   data/ino_data.xml
   ```

---

## 🚀 Step-by-Step Build Instructions

Execute these commands sequentially within your Terminal to configure the SDK path, initialize the local environment, generate the Apple-compliant XML morphology schemas, and compile the bundle:

### 0. Normalize the Apple Developer Kit Path
Apple's compiler utilities often fail if spaces exist in path directories. Use the included helper script to copy and rename your downloaded developer kit into a standardized, space-free system location:
```bash
./setup_sdk.sh
```

### 1. Environment Setup & Dependency Installation
```bash
# Ensure you are inside the repository directory
cd icelandic-dictionary-mac

# Create and activate an isolated Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the core Icelandic BÍN morphology utility engine
pip install islenska
```

### 2. Generate and Build the Bundle
```bash
# Parse the raw ÍNO data and map hundreds of thousands of grammatical syncretisms from BÍN
python3 src/build_dict.py

# Clear any legacy local build caches
make clean

# Compile the binary assets and automatically deploy the final bundle directly into ~/Library/Dictionaries/
make install
```

---

## ⚙️ Activating the Dictionary

Because macOS caches active dictionary databases aggressively inside background system processes, you must manually toggle the registration switch inside the application to see your updates:

1. Completely quit the macOS **Dictionary** application (`Cmd + Q`).
2. Open the **Dictionary** app fresh from your Applications folder or via Spotlight.
3. Open its preference pane by navigating to **Dictionary** ➔ **Settings...** (or **Preferences...**) in the top-left menu bar.
4. Scroll to the absolute bottom of the language checklist.
5. Check the box next to **Íslensk Orðabók**.

> 💡 **Pro-Tip:** You can drag and drop *Íslensk Orðabók* higher up on the checklist priority ladder if you want its definitions to take precedence over standard Apple multilingual dictionaries during system-wide lookups.

---

## 📜 Credits & Licensing
* **Linguistic Definitions:** Derived from the *Íslensk orðabók* dataset curated by the **Stofnun Árna Magnússonar í íslenskum fræðum** (CC BY-NC-ND 4.0).
* **Inflection & Paradigm Arrays:** Powered by the database engine built by **Miðeind ehf** (BÍN handle 373).
* **Toolchain Integration:** Developed and automated by Jonatan Solon.
