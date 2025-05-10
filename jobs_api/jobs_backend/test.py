import requests
import json

# Base URL of your FastAPI application
BASE_URL = "http://192.168.1.2:8000" # Adjust if running on different host/port

def test_get_all_jobs():
    print("Fetching all jobs...")
    response = requests.get(f"{BASE_URL}/test_jobs/")
    if response.ok:
        jobs = response.json()
        print(f"✅ Total jobs fetched: {len(jobs)}, Sample: {jobs}")
        for job in jobs:
            print(f"- {job.get('title')} at {job.get('companyName')} ({job.get('location')})")
    else:
        print(f"❌ Failed to fetch jobs: {response.status_code} - {response.text}")

def test_get_filtered_jobs(company=None, location=None):
    params = {}
    if company:
        params['company'] = company
    if location:
        params['location'] = location

    print(f"Fetching jobs with filters: {params}")
    response = requests.get(f"{BASE_URL}/test_jobs/", params=params)
    if response.ok:
        jobs = response.json()
        print(f"✅ Jobs fetched with filters: {len(jobs)}, Sample: {jobs}")
        for job in jobs:
            print(f"- {job.get('title')} at {job.get('companyName')} ({job.get('location')})")
    else:
        print(f"❌ Failed to fetch filtered jobs: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # test_get_all_jobs()
    print("\n---\n")
    test_get_filtered_jobs(company="Google")
    print("\n---\n")
    # test_get_filtered_jobs(location="Bangalore")
    print("\n---\n")
    test_get_filtered_jobs(company="Microsoft", location="Hyderabad")
