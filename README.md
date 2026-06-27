🇮🇸 macOS Icelandic Monolingual Dictionary Builder
Bring seamless, system-wide Icelandic definitions to your Mac!
This repository provides an automated build pipeline that pairs modern Icelandic definitions from Íslensk nútímamálsorðabók (ÍNO) with the BÍN inflection database. Once compiled, you can use macOS's native Force Click / Three-Finger Tap "Look Up" feature on any heavily inflected Icelandic word (like gleraugunum, viðskiptanna, or borðuðu) inside Safari, Pages, or Mail and instantly see its base dictionary entry.
⚖️ Why This is a "Builder" (License Note)
The underlying definition data provided by Árnastofnun is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).
Because the "NoDerivatives" (ND) clause strictly forbids the distribution of modified or converted versions of the data, pre-compiled .dictionary files cannot legally be hosted here for download. Instead, this project is a fully automated, open-source tool. It allows you to download the official data files directly from the source and compile the dictionary privately on your own Mac for your personal use.
🛠️ Prerequisites
Before building, you will need a few standard developer tools and asset folders on your Mac:
Xcode Command Line Tools: Open your Terminal and run:
Bash
xcode-select --install
Apple Dictionary Development Kit: Download the Additional Tools for Xcode package from the Apple Developer portal. Mount the DMG and copy the DictionaryDevelopmentKit folder into your Utilities folder so it sits exactly at:
Plaintext
/Applications/XcodeAdditionalTools/Utilities/DictionaryDevelopmentKit
Source Dictionary Data: Request or download the official XML export file of the Íslensk nútímamálsorðabók from Árnastofnun. Create a folder named data in this project's root and drop the file inside exactly as:
Plaintext
data/ino_data.xml
🚀 Step-by-Step Build Instructions
Execute these commands in sequence within your Terminal to spin up the local environment, generate the Apple-compliant XML morphology schemas, and execute the native compiler toolchain:
1. Environment Setup & Dependency Installation
Bash
# Ensure you are inside the repository directory
cd icelandic-dictionary-mac

# Create and activate an isolated Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the core Icelandic BÍN morphology utility engine
pip install islenska
2. Generate and Build the Bundle
Bash
# Parse the raw ÍNO data and map hundreds of thousands of grammatical syncretisms from BÍN
python3 src/build_dict.py

# Clear any legacy local build caches
make clean

# Compile the binary assets and automatically deploy the final bundle directly into ~/Library/Dictionaries/
make install
⚙️ Activating the Dictionary
Because macOS caches active dictionary databases aggressively inside background system processes, you must manually toggle the registration switch inside the application to see your updates:
Completely quit the macOS Dictionary application (Cmd + Q).
Open the Dictionary app fresh from your Applications folder or via Spotlight.
Open its preference pane by navigating to Dictionary ➔ Settings... (or Preferences...) in the top-left menu bar.
Scroll to the absolute bottom of the language checklist.
Check the box next to Íslensk Orðabók.
💡 Pro-Tip: You can drag and drop Íslensk Orðabók higher up on the checklist priority ladder if you want its definitions to take precedence over standard Apple multilingual dictionaries during system-wide lookups.
📜 Credits & Licensing
Linguistic Definitions: Derived from the Íslensk orðabók dataset curated by the Stofnun Árna Magnússonar í íslenskum fræðum (CC BY-NC-ND 4.0).
Inflection & Paradigm Arrays: Powered by the database engine built by Miðeind ehf (BÍN handle 373).
Toolchain Integration: Developed and automated by Jonatan Solon.
