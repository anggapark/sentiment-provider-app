import subprocess
import time


def wait_for_postgres(host, max_retries=10, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True,
                env={"PGPASSWORD": "secret"},  # Add password here
            )
            if "accepting connections" in result.stdout:
                print(f"Successfully connected to PostgreSQL at {host}!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL at {host}: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


# Wait for both databases to be ready
if not wait_for_postgres(host="source_postgres"):
    exit(1)
# if not wait_for_postgres(host="destination_postgres"):
#     exit(1)

print("Starting ETL script...")

# Configuration for the source PostgreSQL database
source_config = {
    "dbname": "source_db",
    "user": "postgres",
    "password": "secret",  # Updated to match your docker-compose
    "host": "source_postgres",
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    "pg_dump",
    "-h",
    source_config["host"],
    "-U",
    source_config["user"],
    "-d",
    source_config["dbname"],
    "--no-owner",  # avoid ownership issues
    "--no-acl",  # avoid permission issues
    "-f",
    "data_dump.sql",
    "-w",
]

# Set the PGPASSWORD environment variable to avoid password prompt
subprocess_env = {"PGPASSWORD": source_config["password"]}

print("Executing dump command...")
try:
    # Execute the dump command
    subprocess.run(dump_command, env=subprocess_env, check=True)
    print("Database dump completed successfully...")
except subprocess.CalledProcessError as e:
    print(f"Error during database dump: {e}")
    exit(1)

# Configuration for the destination PostgreSQL database
# destination_config = {
#     "dbname": "destination_db",
#     "user": "postgres",
#     "password": "secret",  # Updated to match your docker-compose
#     "host": "destination_postgres",
# }


# # Use psql to load the dumped SQL file into the destination database
# load_command = [
#     "psql",
#     "-h",
#     destination_config["host"],
#     "-U",
#     destination_config["user"],
#     "-d",
#     destination_config["dbname"],
#     "-a",
#     "-f",
#     "data_dump.sql",
# ]

# # Set the PGPASSWORD environment variable for the destination database
# subprocess_env = {"PGPASSWORD": destination_config["password"]}

# print("Executing load command...")
# try:
#     # Execute the load command
#     subprocess.run(load_command, env=subprocess_env, check=True)
#     print("Data loaded successfully into destination database")
# except subprocess.CalledProcessError as e:
#     print(f"Error during data load: {e}")
#     exit(1)

# print("ETL process completed successfully")
