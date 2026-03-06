# Deploying Shiksha at Your School

This guide is for teachers, school administrators, or volunteers who want to set up Shiksha at their school. Shiksha runs on a single computer and serves the entire school over a local WiFi network — no internet required.

## What You Need

- One desktop or laptop computer (Windows, Linux, or Mac)
- Python 3.8 or higher installed
- A WiFi router (TP-Link or any basic router works)
- Students' devices connected to the same WiFi (phones, tablets, or computers)

## Step 1 — Install Shiksha

Open a terminal and run:
```bash
git clone https://github.com/ShivamDual/shiksha.git
cd shiksha
bash install.sh
```

That's it. The installer will set up everything automatically — virtual environment, dependencies, and the full 507-term database.

## Step 2 — Start the App

Every time you want to run Shiksha:
```bash
cd shiksha
source venv/bin/activate
python shabdakosh/app.py
```

The app will start and show:
```
Running on http://0.0.0.0:5000
```

## Step 3 — Connect Students

Once the app is running, students can open Shiksha on any device connected to the same WiFi.

Find the server computer's IP address:
```bash
hostname -I
```

Tell students to open their browser and go to:
```
http://[IP ADDRESS]:5000
```

For example: `http://192.168.1.5:5000`

No app download needed — it works in any browser.

## Teacher Dashboard

The teacher dashboard shows usage statistics — which terms students search most, daily activity trends, and pending contributions.

- **URL:** `http://localhost:5000/dashboard`
- **Password:** `shiksha2024`

Change the password by editing `dashboard/app.py` line 12.

## Adding New Terms

Teachers and students can submit new terms via the Contribute page at:
```
http://localhost:5000/contribute
```

Submitted terms appear in the dashboard as "Pending Contributions" for teacher review.

## Troubleshooting

**App won't start:**
```bash
cd shiksha
source venv/bin/activate
pip install flask
python shabdakosh/app.py
```

**Students can't connect:**
- Make sure the server computer and student devices are on the same WiFi
- Check the IP address with `hostname -I`
- Make sure no firewall is blocking port 5000

**Database is empty:**
```bash
python shabdakosh/seed_data.py
```

**App crashed:**
- Simply run `python shabdakosh/app.py` again

## Customizing for Your School

Want to add terms in your local language or context? Edit `shabdakosh/seed_data.py` and add new terms following the existing format, then run `python shabdakosh/seed_data.py` again.

## Contact

Built by **Shivam Prasad Raut**, student at Kathmandu Model College, Nepal.
GitHub: [ShivamDual](https://github.com/ShivamDual)

If you deploy Shiksha at your school, I would love to hear about it.