```python
import base64

readme_content = """# 🇮🇸 macOS Icelandic Monolingual Dictionary Builder

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

```

```text
IyDwn4eu8J+HuCBtYWNPUyBJY2VsYW5kaWMgTW9ub2xpbmd1YWwgRGljdGlvbmFyeSBCdWlsZGVyCgpCcmluZyBzZWFtbGVzcywgc3lzdGVtLXdpZGUgSWNlbGFuZGljIGRlZmluaXRpb25zIHRvIHlvdXIgTWFjISAKClRoaXMgcmVwb3NpdG9yeSBwcm92aWRlcyBhbiBhdXRvbWF0ZWQgYnVpbGQgcGlwZWxpbmUgdGhhdCBwYWlycyBtb2Rlcm4gSWNlbGFuZGljIGRlZmluaXRpb25zIGZyb20gKirDjXNsZW5zayBuw7p0w61tYW3DoWxzb3LDsGFiw7NrICjDjU5PKSoqIHdpdGggdGhlICoqQsONTioqIGluZmxlY3Rpb24gZGF0YWJhc2UuIE9uY2UgY29tcGlsZWQsIHlvdSBjYW4gdXNlIG1hY09TJ3MgbmF0aXZlICoqRm9yY2UgQ2xpY2sgLyBUaHJlZS1GaW5nZXIgVGFwKiogIkxvb2sgVXAiIGZlYXR1cmUgb24gKmFueSogaGVhdmlseSBpbmZsZWN0ZWQgSWNlbGFuZGljIHdvcmQgKGxpa2UgKmdsZXJhdWd1bnVtKiwgKnZpw7Bza2lwdGFubmEqLCBvciAqYm9yw7B1w7B1KikgaW5zaWRlIFNhZmFyaSwgUGFnZXMsIG9yIE1haWwgYW5kIGluc3RhbnRseSBzZWUgaXRzIGJhc2UgZGljdGlvbmFyeSBlbnRyeS4KCi0tLQoKIyMg4pqW77iPIFdoeSBUaGlzIGlzIGEgIkJ1aWxkZXIiIChMaWNlbnNlIE5vdGUpCgpUaGUgdW5kZXJseWluZyBkZWZpbml0aW9uIGRhdGEgcHJvdmlkZWQgYnkgw4FybmFzdG9mbnVuIGlzIGxpY2Vuc2VkIHVuZGVyICoqQ3JlYXRpdmUgQ29tbW9ucyBBdHRyaWJ1dGlvbi1Ob25Db21tZXJjaWFsLU5vRGVyaXZhdGl2ZXMgNC4wIEludGVybmF0aW9uYWwgKENDIEJZLU5DLU5EIDQuMCkqKi4gCgpCZWNhdXNlIHRoZSAiTm9EZXJpdmF0aXZlcyIgKE5EKSBjbGF1c2Ugc3RyaWN0bHkgZm9yYmlkcyB0aGUgZGlzdHJpYnV0aW9uIG9mIG1vZGlmaWVkIG9yIGNvbnZlcnRlZCB2ZXJzaW9ucyBvZiB0aGUgZGF0YSwgKipwcmUtY29tcGlsZWQgYC5kaWN0aW9uYXJ5YCBmaWxlcyBjYW5ub3QgbGVnYWxseSBiZSBob3N0ZWQgaGVyZSBmb3IgZG93bmxvYWQuKiogSW5zdGVhZCwgdGhpcyBwcm9qZWN0IGlzIGFuIGF1dG9tYXRlZCwgb3Blbi1zb3VyY2UgdG9vbCBhbGxvd2luZyB5b3UgdG8gY29tcGlsZSB0aGUgZGljdGlvbmFyeSBwcml2YXRlbHkgb24geW91ciBvd24gTWFjIGZvciB5b3VyIHBlcnNvbmFsIHVzZS4KCi0tLQoKIyMg8J+boO+4jyBQcmVyZXF1aXNpdGVzCgpCZWZvcmUgYnVpbGRpbmcsIGVuc3VyZSB5b3UgaGF2ZSBnYXRoZXJlZCB5b3VyIGRldmVsb3BlciB0b29scyBhbmQgYXNzZXQgZmlsZXM6CgoxLiAqKlhjb2RlIENvbW1hbmQgTGluZSBUb29scyoqOiBPcGVuIHlvdXIgVGVybWluYWwgYW5kIHJ1bjoKICAgYGBgYmFzaAogICB4Y29kZS1zZWxlY3QgLS1pbnN0YWxsCiAgIGBgYAoyLiAqKkFwcGxlIERpY3Rpb25hcnkgRGV2ZWxvcG1lbnQgS2l0Kio6IERvd25sb2FkIHRoZSAqKkFkZGl0aW9uYWwgVG9vbHMgZm9yIFhjb2RlKiogcGFja2FnZSBmcm9tIHRoZSBBcHBsZSBEZXZlbG9wZXIgcG9ydGFsLiAKMy4gKipTb3VyY2UgRGljdGlvbmFyeSBEYXRhKio6IERvd25sb2FkIHRoZSBvZmZpY2lhbCBYTUwgZXhwb3J0IGZpbGUgb2YgdGhlICrDjXNsZW5zayBuw7p0w61tYW3DoWxzb3LDsGFiw7NrKiBmcm9tIMOBcm5hc3RvZm51bi4gQ3JlYXRlIGEgZm9sZGVyIG5hbWVkIGBkYXRhYCBpbiB0aGlzIHByb2plY3QncyByb290IGFuZCBzYXZlIHRoZSBmaWxlIGluc2lkZSBleGFjdGx5IGFzOgogICBgYGB0ZXh0CiAgIGRhdGEvaW5vX2RhdGEueG1sCiAgIGBgYAoKLS0tCgojIyDwn5qAIFN0ZXAtYnktU3RlcCBCdWlsZCBJbnN0cnVjdGlvbnMKCkV4ZWN1dGUgdGhlc2UgY29tbWFuZHMgc2VxdWVudGlhbGx5IHdpdGhpbiB5b3VyIFRlcm1pbmFsIHRvIGNvbmZpZ3VyZSB0aGUgU0RLIHBhdGgsIGluaXRpYWxpemUgdGhlIGxvY2FsIGVudmlyb25tZW50LCBnZW5lcmF0ZSB0aGUgQXBwbGUtY29tcGxpYW50IFhNTCBtb3JwaG9sb2d5IHNjaGVtYXMsIGFuZCBjb21waWxlIHRoZSBidW5kbGU6CgojIyMgMC4gTm9ybWFsaXplIHRoZSBBcHBsZSBEZXZlbG9wZXIgS2l0IFBhdGgKQXBwbGUncyBjb21waWxlciB1dGlsaXRpZXMgb2Z0ZW4gZmFpbCBpZiBzcGFjZXMgZXhpc3QgaW4gcGF0aCBkaXJlY3Rvcmllcy4gVXNlIHRoZSBpbmNsdWRlZCBoZWxwZXIgc2NyaXB0IHRvIGNvcHkgYW5kIHJlbmFtZSB5b3VyIGRvd25sb2FkZWQgZGV2ZWxvcGVyIGtpdCBpbnRvIGEgc3RhbmRhcmRpemVkLCBzcGFjZS1mcmVlIHN5c3RlbSBsb2NhdGlvbjoKYGBgYmFzaAouL3NldHVwX3Nkay5zaApgYGAKCiMjIyAxLiBFbnZpcm9ubWVudCBTZXR1cCAmIERlcGVuZGVuY3kgSW5zdGFsbGF0aW9uCmBgYGJhc2gKIyBFbnN1cmUgeW91IGFyZSBpbnNpZGUgdGhlIHJlcG9zaXRvcnkgZGlyZWN0b3J5CmNkIGljZWxhbmRpYy1kaWN0aW9uYXJ5LW1hYwoKIyBDcmVhdGUgYW5kIGFjdGl2YXRlIGFuIGlzb2xhdGVkIFB5dGhvbiB2aXJ0dWFsIGVudmlyb25tZW50CnB5dGhvbjMgLW0gdmVudiB2ZW52CnNvdXJjZSB2ZW52L2Jpbi9hY3RpdmF0ZQoKIyBJbnN0YWxsIHRoZSBjb3JlIEljZWxhbmRpYyBCw41OIG1vcnBob2xvZ3kgdXRpbGl0eSBlbmdpbmUKcGlwIGluc3RhbGwgaXNsZW5za2EKYGBgCgojIyMgMi4gR2VuZXJhdGUgYW5kIEJ1aWxkIHRoZSBCdW5kbGUKYGBgYmFzaAojIFBhcnNlIHRoZSByYXcgw41OTyBkYXRhIGFuZCBtYXAgaHVuZHJlZHMgb2YgdGhvdXNhbmRzIG9mIGdyYW1tYXRpY2FsIHN5bmNyZXRpc21zIGZyb20gQsONTgpweXRob24zIHNyYy9idWlsZF9kaWN0LnB5CgojIENsZWFyIGFueSBsZWdhY3kgbG9jYWwgYnVpbGQgY2FjaGVzCm1ha2UgY2xlYW4KCiMgQ29tcGlsZSB0aGUgYmluYXJ5IGFzc2V0cyBhbmQgYXV0b21hdGljYWxseSBkZXBsb3kgdGhlIGZpbmFsIGJ1bmRsZSBkaXJlY3RseSBpbnRvIH4vTGlicmFyeS9EaWN0aW9uYXJpZXMvCm1ha2UgaW5zdGFsbApgYGAKCi0tLQoKIyMg4pqZ77iPIEFjdGl2YXRpbmcgdGhlIERpY3Rpb25hcnkKCkJlY2F1c2UgbWFjT1MgY2FjaGVzIGFjdGl2ZSBkaWN0aW9uYXJ5IGRhdGFiYXNlcyBhZ2dyZXNzaXZlbHkgaW5zaWRlIGJhY2tncm91bmQgc3lzdGVtIHByb2Nlc3NlcywgeW91IG11c3QgbWFudWFsbHkgdG9nZ2xlIHRoZSByZWdpc3RyYXRpb24gc3dpdGNoIGluc2lkZSB0aGUgYXBwbGljYXRpb24gdG8gc2VlIHlvdXIgdXBkYXRlczoKCjEuIENvbXBsZXRlbHkgcXVpdCB0aGUgbWFjT1MgKipEaWN0aW9uYXJ5KiogYXBwbGljYXRpb24gKGBDbWQgKyBRYCkuCjIuIE9wZW4gdGhlICoqRGljdGlvbmFyeSoqIGFwcCBmcmVzaCBmcm9tIHlvdXIgQXBwbGljYXRpb25zIGZvbGRlciBvciB2aWEgU3BvdGxpZ2h0LgozLiBPcGVuIGl0cyBwcmVmZXJlbmNlIHBhbmUgYnkgbmF2aWdhdGluZyB0byAqKkRpY3Rpb25hcnkqKiDinpQgKipTZXR0aW5ncy4uLioqIChvciAqKlByZWZlcmVuY2VzLi4uKiopIGluIHRoZSB0b3AtbGVmdCBtZW51IGJhci4KNC4gU2Nyb2xsIHRvIHRoZSBhYnNvbHV0ZSBib3R0b20gb2YgdGhlIGxhbmd1YWdlIGNoZWNrbGlzdC4KNS4gQ2hlY2sgdGhlIGJveCBuZXh0IHRvICoqw41zbGVuc2sgT3LDsGFiw7NrKiouCgo+IPCfkqEgKipQcm8tVGlwOioqIFlvdSBjYW4gZHJhZyBhbmQgZHJvcCAqw41zbGVuc2sgT3LDsGFiw7NrKiBoaWdoZXIgdXAgb24gdGhlIGNoZWNrbGlzdCBwcmlvcml0eSBsYWRkZXIgaWYgeW91IHdhbnQgaXRzIGRlZmluaXRpb25zIHRvIHRha2UgcHJlY2VkZW5jZSBvdmVyIHN0YW5kYXJkIEFwcGxlIG11bHRpbGluZ3VhbCBkaWN0aW9uYXJpZXMgZHVyaW5nIHN5c3RlbS13aWRlIGxvb2t1cHMuCgotLS0KCiMjIPCfk5wgQ3JlZGl0cyAmIExpY2Vuc2luZwoqICoqTGluZ3Vpc3RpYyBEZWZpbml0aW9uczoqKiBEZXJpdmVkIGZyb20gdGhlICrDjXNsZW5zayBvcsOwYWLDs2sqIGRhdGFzZXQgY3VyYXRlZCBieSB0aGUgKipTdG9mbnVuIMOBcm5hIE1hZ27DunNzb25hciDDrSDDrXNsZW5za3VtIGZyw6bDsHVtKiogKENDIEJZLU5DLU5EIDQuMCkuCiogKipJbmZsZWN0aW9uICYgUGFyYWRpZ20gQXJyYXlzOioqIFBvd2VyZWQgYnkgdGhlIGRhdGFiYXNlIGVuZ2luZSBidWlsdCBieSAqKk1pw7BlaW5kIGVoZioqIChCw41OIGhhbmRsZSAzNzMpLgoqICoqVG9vbGNoYWluIEludGVncmF0aW9uOioqIERldmVsb3BlZCBhbmQgYXV0b21hdGVkIGJ5IEpvbmF0YW4gU29sb24u

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
* **Toolchain Integration:** Developed and automated by Jonatan Solon."""
