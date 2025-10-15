import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

if __name__ == "__main__":
    run_script('automation_refresh.py')
   