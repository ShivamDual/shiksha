# शिक्षा (Shiksha) — Bilingual STEM Glossary for Rural Nepal

An offline-first bilingual STEM glossary built for students in rural Nepal who study science and mathematics in English but think in Nepali.

## The Problem

In Nepal, STEM subjects are taught in English, but most students in rural areas grow up speaking Nepali. When a student in Karjanha encounters a word like "photosynthesis" or "algorithm" for the first time, there is no quick way to find its Nepali meaning, pronunciation, or a locally relevant example.

Textbooks don't have glossaries. Dictionaries don't have STEM terms. And in schools without reliable internet, Google is not an option.

## The Story Behind Shiksha

I grew up in Mirchaiya, Siraha, a small town in the Terai region of Nepal. My father, who is the Vice Principal of Jansewa Ma Vi Karjanha (School Code: 160560003), a government school in Karjanha Municipality-11, Siraha, has taught there for years. I have watched students struggle not because they lack intelligence, but because they lack access, access to a simple tool that bridges the language gap between how science is taught and how they actually think.

That is why I built Shiksha.

I am currently a high school student at Kathmandu Model College, Bagbazar, Kathmandu. I built this project to solve a real problem for a real school — one I know personally, and one where I plan to deploy this app after exams finish in April 2025.

## What Shiksha Does

Shiksha is a web app that runs entirely offline on a single school computer. Any student on the school's local network can open it in their browser — no installation, no internet required.

- **507 STEM terms** — across Mathematics, Physics, Chemistry, Biology, and Computer Science
- **Bilingual search** — search in English or Nepali (देवनागरी)
- **Nepali pronunciation guides** — for every term
- **Nepal-specific examples** — uses धान, खोला, पहाड, and local contexts students actually recognize
- **Teacher dashboard** — tracks which terms students search most, shows daily usage trends
- **Contribute form** — teachers and students can submit new terms for review

## Who It's For

Built for students across Nepal who face the English-Nepali language gap in STEM education — but specifically designed and intended for deployment at **Jansewa Ma Vi Karjanha**, a government school in Karjanha Municipality, Siraha District. The school serves students from one of Nepal's most underserved rural communities. It has a computer lab but no reliable internet connection.

Shiksha is designed to run on a single desktop computer and serve the entire school over a local WiFi network — no internet required, no subscription, no cost.

## Tech Stack

- **Backend:** Python + Flask
- **Database:** SQLite with FTS5 full-text search
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Search:** Real-time bilingual search (English + Nepali)
- **Deployment:** Offline on local network via TP-Link router

## Installation
```bash
# Clone the repository
git clone https://github.com/ShivamDual/shiksha.git
cd shiksha

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install flask

# Seed the database
python shabdakosh/seed_data.py

# Run the app
python shabdakosh/app.py
```

Open `http://localhost:5000` in any browser. On a local network, replace `localhost` with the server's IP address.

## Features

### Live Bilingual Search
Type in English or Nepali — results appear instantly without page reload using full-text search.

### Subject Browsing
Browse all 507 terms organized by subject: Mathematics (107), Physics (100), Chemistry (100), Biology (100), Computer Science (100).

### Teacher Dashboard
Password protected analytics showing:
- Most searched terms this week
- Daily usage trends
- Total searches and pending contributions

### Contribute Page
Teachers and students can submit new terms with Nepali translations and Nepal-specific examples. Submissions are stored for teacher review before being added.

## Current Status

- ✅ 507 bilingual STEM terms
- ✅ Offline-first architecture
- ✅ Teacher dashboard with usage analytics
- ✅ Real-time bilingual full-text search
- ✅ Mobile-friendly interface
- ⏳ Deployment at Jansewa Ma Vi Karjanha — planned for April 2025

## Author

**Shivam Prasad Raut**
Kathmandu Model College, Bagbazar, Kathmandu
Originally from Mirchaiya-05, Siraha, Nepal
GitHub: [ShivamDual](https://github.com/ShivamDual)