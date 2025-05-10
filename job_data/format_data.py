import json

def convert_to_json_array(input_file, output_file):
    """
    Convert a file with multiple JSON objects into a single JSON array
    
    Args:
        input_file (str): Path to input file with multiple JSON objects
        output_file (str): Path to save the output JSON array
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content into individual JSON objects
    # This assumes each JSON object starts with '{' and ends with '}'
    # and there might be whitespace between them
    json_objects = []
    start = 0
    while True:
        start_brace = content.find('{', start)
        if start_brace == -1:
            break
        end_brace = content.find('}', start_brace)
        if end_brace == -1:
            break
        
        # Extract the JSON object
        json_str = content[start_brace:end_brace+1]
        
        try:
            # Parse the JSON to validate it
            job = json.loads(json_str)
            json_objects.append(job)
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON object: {e}")
        
        start = end_brace + 1
    
    # Write the array of JSON objects to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_objects, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(json_objects)} jobs to JSON array format in {output_file}")

if __name__ == "__main__":
    input_file = r"D:\AIProjects\HIREINN\job_data\job_files\amazon.txt"  # Your current file with multiple JSON objects
    output_file = "jobs_array.json"  # Output file with proper JSON array
    
    convert_to_json_array(input_file, output_file)