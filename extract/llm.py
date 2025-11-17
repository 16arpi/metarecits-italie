import os, sys
from openai import OpenAI



filename = sys.argv[1]

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

print("Creating file...")
file = client.files.create(
    file=open(filename, "rb"),
    purpose="batch"
)

print("Creating batch...")
batch = client.batches.create(
    input_file_id=file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

print(f"Batch created : {batch.id}")
