from app.dal import update_status
from app.core import downloader
from app.queue import transcript_queue
from app.workers import transcript

async def start_download_work(download_data):
    uid = download_data.get("uid", None)
    url = download_data.get("url", None)
    file_id = download_data.get("file_id", None);
    print("Packet got from queue uid = {} \n url = {} \n fileId = {}".format(uid, url, file_id))
    is_update_success = update_status.update_workflow_status(uid, "DOWNLOAD_INPROGRESS")
    if is_update_success:
        wav_file_path = await downloader.download_youtube_podcast(url, file_id)
        print("Path of the wav file {}".format(wav_file_path))
        update_status.update_workflow_status(uid, "DOWNLOAD_COMPLETE")
        transcript_queue.enqueue(transcript.start_transcript_work, download_data, job_timeout=2000)
    else:
        update_status.update_workflow_status(uid, "DOWNLOAD_FAILED")