import pyaudio
import wave
from tqdm import tqdm
import datetime
import random
import os
def all_path(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            result.append(apath)
    return result
csv = []
for i in all_path("./"):
    if "csv" in i:
        csv.append(i[2:])
index = 0
for i in csv:
    index += 1
    print("{}: {}".format(index, i))
time = str(datetime.datetime.now())[:-7]
ch = ""
for i in time:
    if i != "-" and i != ":":
        ch += i
def record(item):
    with open("{}.csv".format(ch), "a") as f:
        f.write("{},{},{},{},{},{},{},{}\n".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
def play_audio(wave_path):
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    stream.stop_stream()
    stream.close()
    p.terminate()
file_input = int(input("选择练习序号："))
file_choose = csv[file_input-1]
with open(file_choose, "r") as f:
    item_list = []
    for line in f:
        item_list.append(line.strip().split(","))
    item_list = item_list[1:]
    random.shuffle(item_list)
for item in item_list:
    answer_list = ["", "A", "B", "C", "D", "E"]
    print("题号：{}/{}".format(item_list.index(item) + 1, len(item_list)))
    print("A. {}".format(item[1]))
    print("B. {}".format(item[2]))
    print("C. {}".format(item[3]))
    print("D. {}".format(item[4]))
    print("E. {}".format(item[5]))
    while True:
        play_audio(item[-1])
        user_input = input("是否需要再听一遍？（键盘a并回车则再次播放）：")
        if user_input not in ["a", "A"]:
            break
    user_answer = str.upper(input("请输入答案："))
    if answer_list.index(user_answer) == int(item[-2]):
        print("回答正确！")
        record_choose = input("是否记录这个题继续练习？（y或者Y代表记录）：")
        if record_choose == "y" or record_choose == "Y":
            record(item)
    else:
        print("错误！")
        record(item)
    next_input = input("是否进入下一题？（回车代表下一题）")
    print("")
