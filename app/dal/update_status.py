import traceback
import psycopg2
from app.db import db_client

def update_workflow_status(uid: int, status_name: str):
  is_update_success = True
  try:
      workflow_state_update_query = """UPDATE podcast_details SET state = %s WHERE id = %s"""
      state_to_update = (status_name, uid)
      cursor = db_client.cursor()
      cursor.execute(workflow_state_update_query, state_to_update)
      # commit changes
      db_client.commit()
      print("Workflow state set to {}".format(status_name))
  except (Exception, psycopg2.Error) as error:
      is_update_success = False
      print("add exception log")
      print(traceback.format_exc())
      print("Failed to insert record into podcast_details table", error)
  finally:
     # closing database connection.
     if db_client:
      cursor.close()
  return is_update_success