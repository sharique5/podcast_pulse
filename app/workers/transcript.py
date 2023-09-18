from app.dal import update_status
from app.core import transcribe
from app.workers import summarize
from app.queue import summarize_queue

async def start_transcript_work(transcript_data):
    try:
        uid = transcript_data.get("uid", None)
        audio_file_name = transcript_data.get("file_id", None);
        print("Packet got from queue uid = {} \n fileId = {}".format(uid, audio_file_name))
        is_update_success = update_status.update_workflow_status(uid, "TRANSCRIPT_INPROGRESS")
        if is_update_success:
            await transcribe.speech_continuous_recognition_old(audio_file_name)
            update_status.update_workflow_status(uid, "TRANSCRIPT_COMPLETE")
            summarize_queue.enqueue(summarize.start_summary_work, transcript_data, job_timeout=2000)
        else:
            update_status.update_workflow_status(uid, "TRANSCRIPT_FAILED")
    except Exception:
        update_status.update_workflow_status(uid, "TRANSCRIPT_FAILED")