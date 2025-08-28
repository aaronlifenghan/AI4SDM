''' We tried to use a dutch emotion classifier, but it's not available on huggingface anymore.'''


from transformers import pipeline
from enum import Enum, auto
from typing import List, Dict

class Language(Enum):
    ENGLISH = auto()
    DUTCH = auto()

class EmotionClassifier:
    def __init__(self, language: Language) -> None:
        if language == Language.DUTCH:
            self.analyzer = pipeline(task='text-classification', model="botdevringring/nl-naxai-ai-emotion-classification-155007122023", tokenizer="botdevringring/nl-naxai-ai-emotion-classification-155007122023", top_k=None, device=1)
            self.tokenizer = self.analyzer.tokenizer
        elif language == Language.ENGLISH:
            self.analyzer = pipeline(task='text-classification', model="tae898/emoberta-base", tokenizer="tae898/emoberta-base", top_k=None, device=1)
            self.tokenizer = self.analyzer.tokenizer
        else:
            raise ValueError("Wrong language selected")
        
        self.tokenMaxLength = self.tokenizer.model_max_length - 5  # Token limit
    
    def cutCandidates(self, text):
        if not isinstance(text, list):
            raise TypeError("Variable is not an array:", text)
        
        candidates = []
        for t in text:
            if self.countTokens(t) > self.tokenMaxLength:
                print("\nSentence too long:", t, flush=True)
                continue
            
            candidates.append(t)

        return candidates

    def getLabel(self, text):
        candidates = self.cutCandidates(text)
        predictions = self.analyzer(candidates)
        return [max(p, key=lambda x: x['score']) for p in predictions]

    
    def getLabels(self, text):
        candidates = self.cutCandidates(text)
        return self.analyzer(candidates)
    
    def getLabelsArray(self, sentences):
        concatenatedText = ""
        results: List[Dict[str, float]] =  [
            {'label': 'neutral', 'score': 0.0},
            {'label': 'surprise', 'score': 0.0},
            {'label': 'sadness', 'score': 0.0},
            {'label': 'anger', 'score': 0.0},
            {'label': 'joy', 'score': 0.0},
            {'label': 'fear', 'score': 0.0},
            {'label': 'disgust', 'score': 0.0}
        ]

        for sentence in sentences:
            if concatenatedText == "" or self.countTokens(concatenatedText + sentence + '\n') <= self.tokenMaxLength:
                concatenatedText += sentence + '\n'
            else:
                result = self.getLabels([concatenatedText])
                if len(result) > 0:
                    results = self.sumLabels(results, result[0])
                    
                concatenatedText = ""
                   
        if len(concatenatedText) > 0:
            result = self.getLabels([concatenatedText])
            if len(result) > 0:
                results = self.sumLabels(results, result[0])
            
        return results
    
    def countTokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text, add_special_tokens=False))
    
    def sumLabels(self, list1: List[Dict[str, float]], list2: List[Dict[str, float]]) -> List[Dict[str, float]]:
        result: Dict[str, float] = {item['label']: item['score'] for item in list1}

        for item in list2:
            label = item['label']
            score = item['score']

            if label in result:
                result[label] += score
            else:
                result[label] = score

        return [{'label': label, 'score': score} for label, score in result.items()]
