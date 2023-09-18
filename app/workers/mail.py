from app.dal import update_status
from app.core import MailService

async def start_email_work(uid, summary_file_name):
    print("Packet got from queue uid = {} \n fileId = {}".format(uid, summary_file_name))
    is_update_success = update_status.update_workflow_status(uid, "EMAIL_INPROGRESS")
    if is_update_success:
        await MailService.send_worker_email(uuid, summary_file_name)
        update_status.update_workflow_status(uid, "EMAIL_COMPLETE")
    else:
        update_status.update_workflow_status(uid, "EMAIL_FAILED")