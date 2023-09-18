from app.dal import update_status
from app.core import summarizer

async def start_summary_work(transcript_data):
    uid = transcript_data.get("uid", None)
    transcript_file_name = transcript_data.get("file_id", None)
    print("Packet got from queue uid = {} \n fileId = {}".format(uid, transcript_file_name))
    is_update_success = update_status.update_workflow_status(uid, "SUMMARY_INPROGRESS")
    if is_update_success:
        await summarizer.summarize_text(transcript_file_name)
        update_status.update_workflow_status(uid, "SUMMARY_COMPLETE")
    else:
        update_status.update_workflow_status(uid, "SUMMARY_FAILED")