from app.dal import update_status
from app.core import transcribe

async def start_transcript_work(transcript_data):
    uid = transcript_data.get("uid", None)
    audio_file_name = transcript_data.get("file_id", None);
    print("Packet got from queue uid = {} \n fileId = {}".format(uid, audio_file_name))
    is_update_success = update_status.update_workflow_status(uid, "TRANSCRIPT_INPROGRESS")
    if is_update_success:
        await transcribe.speech_continuous_recognition_old(audio_file_name)
        # wav_file_path = await downloader.download_youtube_podcast(url, file_id)
        # print("Path of the wav file {}".format(wav_file_path))
        update_status.update_workflow_status(uid, "TRANSCRIPT_COMPLETE")
    else:
        update_status.update_workflow_status(uid, "TRANSCRIPT_FAILED")