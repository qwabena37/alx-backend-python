# 2-main.py
from 0-batch_processing import stream_users_in_batches, batch_processing

if __name__ == "__main__":
    print("Streaming users in batches of 3...\n")
    for batch in stream_users_in_batches(3):
        print("Batch:")
        for user in batch:
            print(user)
        print("-" * 40)

    print("\nProcessing users over age 25...\n")
    batch_processing(3)
