import pickle
with open('/data/MBESLIS/MBESLIS.pkl', 'rb') as file:
   pickleData = pickle.load(file)


import os
from docx import Document

def parse_conversation(doc_path):
    doc = Document(doc_path)
    conversations = []
    current_speaker = None
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text or text.startswith("Consult:"):
            continue
        
        if any(run.bold for run in para.runs):
            current_speaker = 'doctor'
        elif any(run.italic for run in para.runs):
            current_speaker = 'patient'
        else:
            if current_speaker is None:
                continue
        
        if text.startswith("V: "):
            text = text.replace("V: ", "")

        conversations.append([current_speaker, text])
    
    return conversations




ignore_files = [
    '/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/1001_A.docx',
    '/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/1002_A.docx',
    '/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/1003_A.docx',
    '/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/1004 AB_A.docx',
    '/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/1035_A.docx'
]
def list_files_in_folder(folder_path: str):
    files = []
    for file_name in os.listdir(folder_path):
        absolute_path = os.path.join(folder_path, file_name)
        if os.path.isfile(absolute_path) and absolute_path not in ignore_files:
            files.append(absolute_path)
    return files


for d in list_files_in_folder("/data/MBESLIS/data/transfer_2713523_files_60e044cf/Transcripten ABEL/"):
    conversation = parse_conversation(d)
    pickleData.append(conversation)

with open('/data/MBESLIS/MBESLIS.pkl', 'wb') as file:
    pickle.dump(pickleData, file)