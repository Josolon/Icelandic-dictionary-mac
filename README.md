# 🇮🇸 macOS Icelandic Monolingual Dictionary Builder

Bring seamless, system-wide Icelandic definitions to your Mac! 

This repository provides an automated build pipeline that pairs modern Icelandic definitions from **Íslensk nútímamálsorðabók (ÍNO)** with the **BÍN** inflection database. Once compiled, you can use macOS's native **Force Click / Three-Finger Tap** "Look Up" feature on *any* heavily inflected Icelandic word (like *gleraugunum*, *viðskiptanna*, or *borðuðu*) inside Safari, Pages, or Mail and instantly see its base dictionary entry.

---

## ⚖️ Why This is a "Builder" (License Note)

The underlying definition data provided by Árnastofnun is licensed under **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**. 

Because the "NoDerivatives" (ND) clause strictly forbids the distribution of modified or converted versions of the data, **pre-compiled `.dictionary` files cannot legally be hosted here for download.** Instead, this project is a fully automated, open-source tool. It allows you to download the official data files directly from the source and compile the dictionary privately on your own Mac for your personal use.

---

## 🛠️ Prerequisites

Before building, you will need a few standard developer tools on your Mac:

1. **Xcode Command Line Tools**: Open your Terminal and run:
   ```bash
   xcode-select --install
