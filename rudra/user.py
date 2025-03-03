# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from rudra.logging import log_user_activity, log_group_activity
import logging

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

users_collection = db["users"]
groups_collection = db["groups"]

def add_user(user_id):
    try:
        user_id = str(user_id)  
        if not users_collection.find_one({"user_id": user_id}):
            users_collection.insert_one({"user_id": user_id})
            log_user_activity(user_id)
            print(f"User added: {user_id}")
        else:
            print(f"User {user_id} already exists.")
    except Exception as e:
        print(f"Error adding user: {e}")

def add_group(group_id):
    try:
        if not groups_collection.find_one({"group_id": group_id}):
            groups_collection.insert_one({"group_id": group_id})
            logging.info(f"Group added to database: {group_id}")
        else:
            logging.info(f"Group {group_id} already exists in the database.")
    except Exception as e:
        logging.error(f"Error adding group to database: {e}")


def remove_group(group_id):
    try:
        group_id = str(group_id)
        if groups_collection.find_one({"group_id": group_id}):
            groups_collection.delete_one({"group_id": group_id})
            log_group_activity(group_id, action="removed")
            print(f"Group removed: {group_id}")
        else:
            print(f"Group {group_id} not found.")
    except Exception as e:
        print(f"Error removing group: {e}")

def get_user_count():
    try:
        return users_collection.count_documents({})
    except Exception as e:
        print(f"Error fetching user count: {e}")
        return 0

def get_group_count():
    try:
        return groups_collection.count_documents({})
    except Exception as e:
        print(f"Error fetching group count: {e}")
        return 0

def get_all_users():
    try:
        return [user["user_id"] for user in users_collection.find()]
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []

def get_all_groups():
    try:
        return [group["group_id"] for group in groups_collection.find()]
    except Exception as e:
        print(f"Error fetching all groups: {e}")
        return []