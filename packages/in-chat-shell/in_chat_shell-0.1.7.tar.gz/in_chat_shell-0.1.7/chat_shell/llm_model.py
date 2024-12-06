import requests
import logging
import json
from typing import Optional, Generator, Union
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class LLMAPIError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def chat_completions(
    messages: list, 
    timeout: int = 30, 
    provider="azure-openai", 
    model="gpt-4o", 
    temperature=1.0, 
    stream=False
) -> Union[str, Generator[str, None, None]]:
    """
    调用GPT-4 API的函数，支持流式输出
    
    Args:
        messages (list): 消息列表
        timeout (int): 请求超时时间（秒）
        provider (str): API提供者
        model (str): 模型名称
        temperature (float): 温度参数
        stream (bool): 是否使用流式输出
    
    Returns:
        Union[str, Generator[str, None, None]]: 
            如果stream=True，返回生成器
            如果stream=False，返回完整响应字符串
    """
    url = "https://dev-outside-ai-service.smzdm.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer smart_shell_test",
        "Z-PROVIDER-NAME": provider,
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream
    }

    try:
        logger.info("Sending request to GPT API")
        response = requests.post(
            url, 
            headers=headers, 
            json=data,
            timeout=timeout,
            stream=stream
        )
        
        response.raise_for_status()
        
        if stream:
            def generate_stream():
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        line = line.decode('utf-8')
                        if not line.startswith('data: '):
                            continue
                            
                        json_str = line[6:].strip()  # 移除 "data: " 前缀
                        if json_str == "[DONE]":
                            break
                            
                        response_data = json.loads(json_str)
                        
                        # 检查响应格式
                        if not response_data.get("choices"):
                            logger.info(f"Unexpected response format: {response_data}")
                            continue
                            
                        choice = response_data["choices"][0]
                        if choice.get("finish_reason"):
                            break
                            
                        if "delta" not in choice:
                            logger.info(f"Delta not found in choice: {choice}")
                            continue
                            
                        content = choice["delta"].get("content", "")
                        if content:
                            yield content
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON decode error: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Error processing stream: {e}")
                        continue

            return generate_stream()
        else:
            # 非流式响应处理
            response_data = response.json()
            
            if not response_data.get("choices"):
                raise LLMAPIError("Invalid API response format: 'choices' not found")
            
            if not response_data["choices"]:
                raise LLMAPIError("Empty choices in API response")
                
            content = response_data["choices"][0].get("message", {}).get("content")
            if content is None:
                raise LLMAPIError("Content not found in API response")
                
            return content

    except requests.exceptions.Timeout:
        error_msg = "Request timed out"
        logger.error(error_msg)
        raise LLMAPIError(error_msg)
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {str(e)}"
        logger.error(error_msg)
        raise LLMAPIError(error_msg)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        logger.error(error_msg)
        raise LLMAPIError(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        raise LLMAPIError(error_msg)

# 测试用例
if __name__ == "__main__":
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    try:
        # 测试流式输出
        print("Testing streaming output:")
        for chunk in chat_completions(test_messages, stream=True):
            print(chunk, end='', flush=True)
        print("\n")
        
        # 测试非流式输出
        print("Testing non-streaming output:")
        response = chat_completions(test_messages, stream=False)
        print(response)
        
    except LLMAPIError as e:
        print(f"Error: {e}")