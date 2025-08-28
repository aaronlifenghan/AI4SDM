from LLM import LLM
from pathlib import Path
from tqdm import tqdm
import pickle
import sys

CONVERSATION_COUNT = 5
ROUNDS = 100
SYSTEM_PROMPTS_INDEX = [6] #[1, 2, 3, 4, 5, 6, 7, 8]


def getResponseBase():
    responseBase = Path(f"response")

    responseCounter = 1
    while responseBase.exists():
        responseBase = Path(f"response{responseCounter}")
        responseCounter += 1
        
    return responseBase


def getConversations():    
    src = Path("/home/s3366952/master-thesis/datasets/MBESLIS/MBESLIS.pkl")
    with src.open('rb') as file:
        loadedData = pickle.load(file)

    conversations = []

    conversationCounter = 0
    for conversation in loadedData:
        conversationStr = ""
        for speaker, sentence in conversation:
            conversationStr += f"{speaker}: {sentence}"

        conversations.append('"' + conversationStr + '"')
        conversationCounter += 1
        if conversationCounter >= CONVERSATION_COUNT:
            return conversations

    return conversations

def saveConversations(folder: Path, conversations):
    folder.mkdir(parents=True)
    for i, conversation in enumerate(conversations, start=1):
        conversationFile = folder / Path(f"conversation_{i}.txt")
        conversationFile.write_text(conversation)

def main():
    if sys.argv[1] != "startedinbash":
        print("Start using bash file!")
        exit()

    llm = LLM("meta-llama/Llama-3.1-8B-Instruct")

    responseBase = getResponseBase()
    conversations = getConversations()

    saveConversations(responseBase / Path("conversations"), conversations)

    progressBar = tqdm(total=ROUNDS * len(SYSTEM_PROMPTS_INDEX), ncols=50)

    for j in range(1, ROUNDS + 1):
        for promptIndex in SYSTEM_PROMPTS_INDEX:
            systemPromptFile = Path(f"systemprompt/prompt_{promptIndex}.txt")
            responseFile = responseBase / Path(str(j)) / Path(f"response_{promptIndex}.txt")

            generatedTexts = llm.generateTexts(systemPromptFile.read_text(encoding="utf-8"), conversations)

            responseFile.parent.mkdir(exist_ok=True, parents=True)
            responseFile.write_text("\n".join(generatedTexts), encoding="utf-8")

            if progressBar.update():
                print("")

if __name__ == "__main__":
    main()