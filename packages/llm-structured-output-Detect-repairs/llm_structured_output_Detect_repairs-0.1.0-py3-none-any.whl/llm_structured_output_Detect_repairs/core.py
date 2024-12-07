# llm_structured_output_Detect_repairs/core.py

import os
import sys
import requests
import json
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.chat_models import ChatOpenAI
from typing import Dict, Any, List

def load_project_lib():
    cwd = os.getcwd()
    project_name = 'lfl_llm_agent'
    project_base = cwd.split(project_name)[0]
    project_lib = os.path.join(project_base, project_name, 'apps')
    sys.path.append(project_lib)

load_project_lib()
from json_repair import repair_json
# 发送消息到 Ollama
def send_message_to_ollama(message, port=11434):
    url = f"http://192.168.31.160:{port}/api/chat"
    payload = {
        "model": "qwen2.5:14b",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_content = ""
        for line in response.iter_lines():
            if line:
                response_content += json.loads(line)["message"]["content"]
        return response_content
    else:
        return f"Error: {response.status_code} - {response.text}"

# 解析千问模型的输出
def parse_tongyi_output(output: str):
    data = output.replace("```", "").replace("json", "")
    return data

def structured_output(model_name: str = "openai", temperature: float = 0.0, question: str = "北京的首都？") -> Dict[str, Any]:
    """
    使用 Langchain 的 StructuredOutputParser 和 PromptTemplate 控制结构化数据输出为 JSON。
    """
    stories_schemas = {
        "datetime": {"type": "str", "description": "datetime of story"},
        "story": {"type": "str", "description": "details of the story"},
    }

    response_schemas = [
        {"name": "name", "description": "name of people", 'type': 'str'},
        {"name": "age", "description": "age of person", 'type': 'int'},
        {
            "name": "stories",
            "description": "all stories in the life, list of story details",
            'type': 'list',
            "schema": stories_schemas
        },
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt_template = PromptTemplate(
        template="尽可能好的回答用户的问题。\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions},
    )

    if model_name == "openai":
        model = ChatOpenAI(temperature=temperature, openai_api_key='sk-proj-gFxygSMQV0IbofUcU8N7T3BlbkFJwiZf7eglUJvxmxHCsEgI')
        _input = prompt_template.format(question=question)
        output = model.invoke(_input)
        output_str = output if isinstance(output, str) else output.content
        return output_parser.parse(output_str)

    elif model_name == "tongyi":
        response_content = send_message_to_ollama(prompt_template.format(question=question))
        parsed_output = parse_tongyi_output(response_content)
        return output_parser.parse(parsed_output)

    else:
        raise ValueError("无效的模型名称。请选择 'openai' 或 'tongyi'")

def check_and_repair_json(result):
    try:
        json_data = json.loads(result)
        print(f"模型结果是有效的 JSON 格式: {json_data}")
        return json_data
    except json.JSONDecodeError:
        print("模型结果不是有效的 JSON 格式，尝试修复...")
        repaired_json = repair_json(result)
        try:
            json_data = json.loads(repaired_json)
            print(f"模型结果异常 JSON 修复成功: {json_data}")
            return json_data
        except json.JSONDecodeError:
            print("模型结果异常 JSON 修复失败")
            return None

if __name__ == "__main__":
    model_name = "openai"
    result = structured_output(model_name=model_name, question="习近平主席简介？")
    print(f"模型结果: {result}")
    if model_name == "openai":
        if isinstance(result, dict):
            print("模型结果是正常的 JSON 字典，无需修复")
        else:
            print(f"模型结果不是有效的 JSON 格式: {result}")
            check_and_repair_json(result)
    elif model_name == "tongyi":
        check_and_repair_json(result)