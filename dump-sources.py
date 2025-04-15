import os
import pandas as pd
from util.env import SOURCE
from util.mongo import source_cursor
from util.logger import logger
from util.s3 import store_output_in_s3_versioned

CHUNK_SIZE = 10_000


def handle_batch(batch: list, sequence: int, local_file_path: str):
    logger.info(f"Running chunk {sequence}")
    df = pd.DataFrame.from_dict(batch)

    mode = 'a' if sequence > 0 else 'w'
    header = sequence == 0

    df.to_csv(local_file_path, index=False, header=header, sep=";", mode=mode)
    logger.info(f"Generated CSV for chunk {sequence}")


def main():
    logger.info("Starting run")

    cursor = source_cursor(SOURCE)

    local_file_path = f"output/tmp.csv"

    batch = []
    batches_handled = 0
    index = 0
    for entry in cursor:
        batch.append(entry)
        index += 1

        if index == CHUNK_SIZE:
            handle_batch(batch, batches_handled, local_file_path)
            batches_handled += 1
            batch = []
            index = 0

    # Handle last batch
    handle_batch(batch, batches_handled, local_file_path)

    # Store in S3 (latest and versioned)
    store_output_in_s3_versioned(
        file_path=local_file_path, kind="source", base_file_name=SOURCE, extension='csv'
    )

    # Remove tmp file
    os.remove(local_file_path)


    total_documents = batches_handled * CHUNK_SIZE + len(batch)
    logger.info(
        f"{total_documents} documents processed in {batches_handled + 1} batches"
    )


if __name__ == "__main__":
    main()
