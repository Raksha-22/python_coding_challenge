# python_coding_challenge
Implementation of python based coding challenge as part of technical assesment.

# Link for mysql dump file
https://drive.google.com/drive/folders/1FVUgfab5MUUGY5a1y1RVZitbIuz-vGlX?usp=drive_link

# If you are using MYSQL-->import database using .sql file
mysql -u root -p your_database_name < gutenberg_dump.sql

# Clone the Repository Locally
1. Create a folder locally
2. Open terminal in that folder
3. Initialize Git in the folder:
   git init
4. Add the remote origin (replace <repo-url> with your actual repository URL):
   git remote add origin <repo-url>
5. Verify the remote:
   git remote -v
6. Pull the latest code from the main branch:
   git pull origin main

# Install Requirements
Install the required packages:
   pip install -r requirements.txt

# Set Up Virtual Environment (Optional but Recommended)
1. Create a virtual environment:
   python -m venv venv
2. Activate the virtual environment (on Windows):
   venv\Scripts\activate

# Run the Application
python app.py
