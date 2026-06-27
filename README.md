# Icelandic-dictionary-mac
Create .dictionary files for the native macOS dictionary look up function
# 🇮🇸 macOS Icelandic Monolingual Dictionary

Bring system-wide Icelandic definitions to your Mac! This project parses open-access lexicographical data from **Árnastofnun** and pairs it with the **BÍN** inflection database. 

The result? You can use macOS's native **Force Click / Three-Finger Tap** "Look Up" feature on *any* inflected Icelandic word (like *hestinum*, *gleraugunum*, or *skrifuðu*) inside Safari, Pages, or Mail, and instantly see its base definition.

---

## 🚀 Quick Installation (For Regular Users)

You do not need to run any code to use this dictionary!

1. Go to the **[Releases](../../releases)** page of this repository and download the latest `Icelandic.dictionary.zip`.
2. Unzip the file on your Mac.
3. Open **Finder**, press `Cmd + Shift + G`, paste `~/Library/Dictionaries/`, and hit Enter.
4. Drag and drop the unzipped `Icelandic.dictionary` file into that folder.
5. Open the native **Dictionary** app on your Mac, go to **Settings** (or **Preferences**), scroll to the bottom, and check the box next to **Íslensk Orðabók** to activate it.

---

## 🛠️ Developer Setup & Building From Source

If you want to modify the parsing logic or compile the dictionary yourself, follow these steps:

### Prerequisites
* A Mac running macOS with Xcode or Xcode Command Line Tools installed.
* **Dictionary Development Kit**: Download "Additional Tools for Xcode" from the Apple Developer portal and copy the Dictionary Development Kit folder into this project.
* Python 3.x

### How to Build
1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/mac-icelandic-dictionary.git](https://github.com/YOUR_USERNAME/mac-icelandic-dictionary.git)
   cd mac-icelandic-dictionary
