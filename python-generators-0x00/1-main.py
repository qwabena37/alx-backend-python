from 0-stream_users import stream_users


if __name__ == "__main__":
    print("Streaming users from user_data table...\n")
    
    for user in stream_users():
        print(user)