import os
from dotenv import load_dotenv
load_dotenv()

from typing import Optional

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "azure").lower()


def call_llm(prompt: str, system: Optional[str] = None, temperature: float = 0.2) -> str:
    if LLM_PROVIDER == "azure":
        return _call_azure_openai(prompt, system, temperature)
    elif LLM_PROVIDER == "bedrock":
        return _call_bedrock(prompt, system, temperature)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")


def _call_azure_openai(prompt, system, temperature):
    from openai import AzureOpenAI
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=deployment, messages=messages, temperature=temperature)
    return response.choices[0].message.content


def _call_bedrock(prompt, system, temperature):
    import boto3
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")
    kwargs = {
        "modelId": model_id,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"temperature": temperature, "maxTokens": 1000},
    }
    if system:
        kwargs["system"] = [{"text": system}]
    response = client.converse(**kwargs)
    return response["output"]["message"]["content"][0]["text"]


if __name__ == "__main__":
    print(f"Using provider: {LLM_PROVIDER}")
    print(call_llm("Say hello in one short sentence."))