import torch
from transformers import pipeline
from huggingface_hub import login

class LLM:
    def __init__(self, model_id):
        login("XXXX")

        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def generateTexts(self, systemPrompt, userPrompts):
        messages = []

        for userPrompt in userPrompts:
            message = [{"role": "system", "content": systemPrompt}, {"role": "user", "content": userPrompt}]
            messages.append(message)

        outputs = self.pipe(messages, max_new_tokens=8192)
        
        generatedTexts = []

        for output in outputs:
            for generatedText in output[0]["generated_text"]:
                if generatedText["role"] != "assistant":
                    continue

                generatedTexts.append(generatedText["content"])
                break

        if len(generatedTexts) != len(userPrompts):
            raise Exception(f"Generated text was different size than user prompts. Count text: {len(generatedTexts)} Count Prompts: {len(userPrompts)}")

        return generatedTexts

