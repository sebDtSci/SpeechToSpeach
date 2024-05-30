import ollama
import time

nouveauTypage:str  = "test"

def generate(prompt: str, model_name: str) -> str:
    startTime = time.time()
    res = ollama.generate(
        model=model_name,
        prompt=prompt
    )
    endtime = time.time()
    exTime = endtime - startTime
    return res, exTime

if __name__ == "__main__":
    res, exeTime = generate("Bonjour", "gemma")
    print(res['response'])
    print(f"Temps de génération : {exeTime} secondes")
    print(res['total_duration'])