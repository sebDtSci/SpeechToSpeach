import ollama
import time

# nouveauTypage:str  = "test"

def generate(prompt: str, model_name: str) -> str:
    """
    Generates text using the specified prompt and model.

    Args:
        prompt (str): The prompt to generate text from.
        model_name (str): The name of the model to use for text generation.

    Returns:
        tuple[str, float]: A tuple containing the generated text and the execution time in seconds.
    """
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