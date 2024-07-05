import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer
from anthropic import Anthropic
import openai

def get_model(model_name: str):
    if model_name.startswith("ollama/"):
        return dspy.OllamaClient(model=model_name.split("/")[1])
    elif model_name.startswith("hf/"):
        model_id = model_name.split("/", 1)[1]
        model = AutoModelForCausalLM.from_pretrained(model_id)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        return dspy.HFTorchClient(model, tokenizer)
    elif model_name == "anthropic/claude":
        anthropic = Anthropic()
        return dspy.AnthropicClient(api_key=anthropic.api_key)
    elif model_name == "openai/gpt-4":
        return dspy.OpenAIClient(api_key=openai.api_key, model="gpt-4")
    else:
        raise ValueError(f"Unsupported model: {model_name}")