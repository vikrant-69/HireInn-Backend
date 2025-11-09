import requests
import json

# Base URL of your FastAPI application
# --------------------------------------------------------------------------
# IMPORTANT: Change this to "http://127.0.0.1:8000" if you are running
# the FastAPI server and this script on the same machine.
# --------------------------------------------------------------------------
BASE_URL = "http://192.168.1.4:8002" 

def test_get_all_jobs():
    """Tests fetching all jobs without any filters."""
    print("--- Test Case 1: Fetching all jobs ---")
    
    # Corrected endpoint path from "/test_jobs/" to "/jobs_v1/"
    endpoint = f"{BASE_URL}/JOBS_V1/"
    
    try:
        response = requests.get(endpoint)
        
        # Check if the request was successful
        response.raise_for_status() 

        jobs = response.json()
        print(f"✅ Success! Fetched {len(jobs)} jobs.")
        
        if jobs:
            print("Sample job data:")
            # Use the correct field names as defined in the Job model
            for job in jobs[:2]: # Print first 2 jobs as samples
                job_title = job.get('job_title')
                company = job.get('company')
                location = job.get('location')
                job_id = job.get('id')
                print(f"  - ID: {job_id}\n    Title: {job_title}\n    Company: {company}\n    Location: {location}\n")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: An error occurred while making the request: {e}")
    except json.JSONDecodeError:
        print(f"❌ FAILED: Could not decode JSON response. Status: {response.status_code}, Body: {response.text}")


def test_get_jobs_with_filters():
    """Tests fetching jobs using query parameters for filtering."""
    print("\n--- Test Case 2: Fetching jobs with filters ---")
    
    # Define filters to test
    params = {
        "company": "Goldman",  # Using a partial name for regex search
        "location": "Hyderabad"
    }
    
    endpoint = f"{BASE_URL}/jobs_v1/"
    print(f"Querying with params: {params}")

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        jobs = response.json()
        print(f"✅ Success! Found {len(jobs)} jobs matching the criteria.")
        
        for job in jobs:
            # All jobs returned should match the filter criteria
            assert "goldman" in job.get('company', '').lower()
            assert "hyderabad" in job.get('location', '').lower()

        if jobs:
            print("Sample of filtered result:")
            job = jobs[0]
            job_title = job.get('job_title')
            company = job.get('company')
            location = job.get('location')
            print(f"  - Title: {job_title}\n    Company: {company}\n    Location: {location}\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: An error occurred while making the request: {e}")
    except AssertionError:
        print("❌ FAILED: The returned data did not match the filter criteria.")


if __name__ == "__main__":
    test_get_all_jobs()
    # test_get_jobs_with_filters()