from app.dal import update_status
from app.core import summarizer
from app.queue import mailer_queue
from app.workers import mailer

async def start_summary_work(summary_data):
    try:
        uid = summary_data.get("uid", None);
        transcript_file_name = summary_data.get("file_id", None);
        print("Packet got from queue uid = {} \n fileId = {}".format(uid, transcript_file_name))
        is_update_success = update_status.update_workflow_status(uid, "SUMMARY_INPROGRESS")
        if is_update_success:
            await summarizer.summarize_text(transcript_file_name)
            update_status.update_workflow_status(uid, "SUMMARY_COMPLETE")
            mailer_queue.enqueue(mailer.start_mailer_work, summary_data);
        else:
            update_status.update_workflow_status(uid, "SUMMARY_FAILED")
    except Exception:
        update_status.update_workflow_status(uid, "SUMMARY_FAILED")