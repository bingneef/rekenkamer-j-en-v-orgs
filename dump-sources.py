import os
import pandas as pd
from util.env import SOURCE
from util.mongo import source_cursor
from util.logger import logger
from util.s3 import store_output_in_s3

CHUNK_SIZE = 10000


def handle_batch(batch: list, sequence: int):
    logger.info(f"Running chunk {sequence}")
    df = pd.DataFrame.from_dict(batch)

    local_file_path = f"output/tmp_{sequence}.xlsx"
    df.to_excel(local_file_path, index=False)
    logger.info(f"Generated Excel for chunk {sequence}")

    base_file_name = f"dump_{sequence}"
    if SOURCE != "":
        base_file_name = f"{SOURCE}_{base_file_name}"

    store_output_in_s3(
        file_path=local_file_path, kind="source", base_file_name=base_file_name
    )

    # Remove tmp file
    os.remove(local_file_path)


def main():
    logger.info("Starting run")

    cursor = source_cursor(SOURCE)

    batch = []
    batches_handled = 0
    index = 0
    for entry in cursor:
        batch.append(entry)
        index += 1

        if index == CHUNK_SIZE:
            handle_batch(batch, batches_handled)
            batches_handled += 1
            batch = []
            index = 0

    # Handle last batch
    handle_batch(batch, batches_handled)

    total_documents = batches_handled * CHUNK_SIZE + len(batch)
    logger.info(
        f"{total_documents} documents processed in {batches_handled + 1} batches"
    )


if __name__ == "__main__":
    main()
