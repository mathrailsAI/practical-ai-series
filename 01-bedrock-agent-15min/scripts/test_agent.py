#!/usr/bin/env python3
import boto3
import sys

# Configuration - Replace with your values
AGENT_ID = 'YOUR_AGENT_ID'
ALIAS_ID = 'YOUR_ALIAS_ID'
REGION = 'YOUR_REGION'
# AWS Credentials - For testing only
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'
class BedrockAgentTester:
    def __init__(self, agent_id, alias_id, region, access_key, secret_key):
        self.client = boto3.client(
            'bedrock-agent-runtime',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.agent_id = agent_id
        self.alias_id = alias_id

    def chat(self, message):
        response = self.client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.alias_id,
            sessionId='test-session',
            inputText=message
        )

        result = ""
        for event in response['completion']:
            if 'chunk' in event and 'bytes' in event['chunk']:
                result += event['chunk']['bytes'].decode('utf-8')
        return result
if __name__ == '__main__':
    agent = BedrockAgentTester(AGENT_ID, ALIAS_ID, REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    while True:
        query = input("You: ").strip()
        if query in ['/quit', 'exit']:
            break
        response = agent.chat(query)
        print(f"Agent: {response}\n")