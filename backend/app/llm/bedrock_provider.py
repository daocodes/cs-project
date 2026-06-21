import json

import boto3

from app.llm.provider import LLMProvider


class BedrockProvider(LLMProvider):
    def __init__(self, region: str, model_id: str):
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def invoke(self, prompt: str) -> str:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
        response = self.client.invoke_model(modelId=self.model_id, body=body)
        payload = json.loads(response["body"].read())
        return payload["content"][0]["text"]
