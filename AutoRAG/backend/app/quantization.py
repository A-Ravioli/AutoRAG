import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def quantize_model(model_name: str):
    # Load the model
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Quantize the model
    quantized_model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )

    # Save the quantized model
    quantized_model.save_pretrained("./quantized_model")
    tokenizer.save_pretrained("./quantized_model")

    return "./quantized_model"