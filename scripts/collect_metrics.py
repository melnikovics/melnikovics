import logging

# Attempt to import commits, handle ImportError if necessary
try:
    import commits
except ImportError:
    logging.error("Failed to import 'commits' module. Ensure commits.py is in the scripts directory.", exc_info=True)
    commits = None # Set to None so later checks can skip if import failed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

def run_commits_script():
    """Runs the commits.py script and logs its execution."""
    if commits:
        try:
            logging.info("Running commits.py script...")
            commits.main()
            logging.info("commits.py script completed successfully.")
        except Exception as e: # Keep original exception logging detail
            logging.error(f"Error running commits.py: {e}", exc_info=True)
    else:
        logging.warning("Skipping commits.py execution due to import failure.")

if __name__ == "__main__":
    logging.info("Starting metrics collection process (GitHub commits only)...")
    run_commits_script()
    logging.info("Metrics collection process finished (GitHub commits only).")
