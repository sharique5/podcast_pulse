import traceback
import psycopg2
from app.db import db_client

def get_recipient_email(uid: int):
  try:
      workflow_state_get_email_query = """SELECT email FROM podcast_details WHERE file_id = %s"""
      state_to_update = (uid)
      cursor = db_client.cursor()
      email = cursor.execute(workflow_state_get_email_query, state_to_update)
      # commit changes
      db_client.commit()
      print("Selected email is {}".format(email))
  except (Exception, psycopg2.Error) as error:
      print("add exception log")
      print(traceback.format_exc())
      print("Failed to fetch record into podcast_details table", error)
  finally:
     # closing database connection.
     if db_client:
      cursor.close()
  return email