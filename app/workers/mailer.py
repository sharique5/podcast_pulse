import os
from app.dal import update_status
from app.core import mailer

async def start_mailer_work(mailing_data):
  try:
      uid = mailing_data.get("uid", None);
      email = mailing_data.get("email", None);
      file_id = mailing_data.get("file_id", None);
      curr_dir = os.path.dirname(os.path.abspath(__file__))
      summary_file_path = os.path.normpath(os.path.join(curr_dir, "../", "../", "summary", f"{file_id}.txt"))
      print("Packet got from queue uid = {} \n email = {}".format(uid, email))
      is_update_success = update_status.update_workflow_status(uid, "MAIL_INPROGRESS")
      if is_update_success:
        mailer.sendEmail(email, summary_file_path)
        update_status.update_workflow_status(uid, "MAIL_COMPLETE")
      else:
        update_status.update_workflow_status(uid, "MAIL_FAILED")
  except Exception:
    update_status.update_workflow_status(uid, "MAIL_FAILED")