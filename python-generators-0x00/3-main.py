# 3-main.py
from 2-lazy_paginate import paginate_users, lazy_pagination

if __name__ == "__main__":
    print("Fetching a single page of users (page size = 3, offset = 0)...\n")
    page = paginate_users(3, 0)
    for user in page:
        print(user)
    
    print("\nLazy pagination over all users (page size = 3)...\n")
    for page_num, page in enumerate(lazy_pagination(3), start=1):
        print(f"Page {page_num}:")
        for user in page:
            print(user)
        print("-" * 40)
