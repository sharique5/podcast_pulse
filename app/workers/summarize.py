from app.dal import update_status
from app.core import summarizer
from app.workers import mail
from app.queue import mailer_queue

async def start_summary_work(uid, transcript_file_name):
    print("Packet got from queue uid = {} \n fileId = {}".format(uid, transcript_file_name))
    is_update_success = update_status.update_workflow_status(uid, "SUMMARY_INPROGRESS")
    if is_update_success:
        await summarizer.summarize_text(transcript_file_name)
        update_status.update_workflow_status(uid, "SUMMARY_COMPLETE")
        mailer_queue.enqueue(mail.send_worker_email, uid, transcript_file_name, job_timeout=2000)
    else:
        update_status.update_workflow_status(uid, "SUMMARY_FAILED")