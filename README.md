# DepressionApp

## Description
DepressionApp is an application designed to guide depressed patients through their illness while assisting doctors in tracking symptoms and improving treatment strategies. The app aims to enhance the treatment process by providing symptom monitoring, treatment adherence tracking, and motivational support for patients.

## Current Features
- **Symptom Tracking:** Patients can log their symptoms over time to observe trends.
- **Patient Dashboard:** Patients have access to a visual trajectory of their symptoms to better understand their mental health progress.
- **Doctor Dashboard:** Doctors can view their patients’ symptom trajectories, allowing for more informed and data-driven assessments.

## Planned Features
- **Treatment Adherence Tracking:** Tracks medication intake, therapy sessions, and exercises.
- **Correlation Analysis:** Relates symptoms to treatment adherence to identify effective interventions.
- **Guided Exercises:** Provides patients with therapeutic exercises and self-help strategies.
- **Patient Dashboard:** Provides an overview of treatment adherence and relate it to symptom trajectory.
- **Doctor Dashboard:** Enables doctors to see treatment adherence and symptom trajectories, improving diagnostic reliability by considering long-term trends instead of single-day assessments.

## Tech Stack
- **Programming Language:** Python
- **Framework:** Django
- **Database:** SQLite

## Installation & Usage
This project runs on ``Python 3.13.2``. Follow the steps below to get started.

### Prerequisites:
- ``Python 3.13.2`` installed on your system
- ``Git`` (optional, if cloning the repo)

Assuming you are in the root directory of this project, run the following commands in your terminal:
```bash
python -m venv testenv # Create and activate a virtual environment

testenv\Scripts\activate  # On Windows
# For macOS/Linux, use: source testenv/bin/activate

pip install -r requirements.txt # Install dependencies

cd depressionApp # Navigate to the Django app directory

python manage.py runserver # Run the server
```
Once the server is running, open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You can log in using any of the following test users:
| Username   | Password   |
|------------|------------|
| `doc1`     | `123passwd` |
| `doc2`     | `123passwd` |
| `patient1` | `123passwd` |
| `patient2` | `123passwd` |
