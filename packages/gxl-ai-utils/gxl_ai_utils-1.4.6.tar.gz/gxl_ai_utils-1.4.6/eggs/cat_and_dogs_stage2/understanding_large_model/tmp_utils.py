from tqdm import tqdm

from gxl_ai_utils.utils import utils_file

def do_get_formatted_datalist_for_asr_task(input_text, input_wav, dataset_name):
    """
    这个函是为了给实验室理解大模型任务中要用到的数据生成标准格式的data.list
    标准格式:
      {
  "task": task_tag, # 如 "<TRANSCRIBE>"
  "key":  utt_id, # 如 "IC0001W0007"
  "wav": wav_path, # 如 "/home/backup_nfs/data-ASR/AIShell2/AISHELL-2/iOS/data/wav/C0001/IC0001W0007.wav"
  "txt": text, # 如 "天安门"
  "lang": language, # 如 "<CN>"
  "speaker": speaker_tag, # 如 "spk001"
  "emotion": emotion等分类标签 # 如 "<HAPPY>"
  "gender": 性别标签 # 如 "<MALE>"
  "extra":{class:"label", "duration": wav_length# 单位s，如2.05125，表示2.05秒}
  }

    :param input_text:
    :param input_wav:
    :return:
    """
    if not isinstance(input_wav, dict):
        assert isinstance(input_wav, str)
        input_wav = utils_file.load_dict_from_scp(input_wav)
    if not isinstance(input_text, dict):
        assert isinstance(input_text, str)
        input_text = utils_file.load_dict_from_scp(input_text)
    task_tag = "<TRANSCRIBE>"
    lang = "<CN>" if "librispeech" not in dataset_name else "<EN>"
    speaker = "<NONE>"
    emotion  = "NEUTRAL"
    gender = "<NONE>"
    res_list = []
    for key, wav_path in tqdm(input_wav.items(), desc="Generating formatted data.list for ASR task", total=len(input_wav)):
        txt = input_text[key]
        extra = {"duration": utils_file.do_get_wav_duration(wav_path), "dataset": dataset_name}
        item_dict = {"task": task_tag, "key": key, "wav": wav_path,"txt": txt, "lang": lang, "speaker": speaker, "emotion": emotion, "gender": gender, "extra": extra}
        res_list.append(item_dict)
    return res_list
