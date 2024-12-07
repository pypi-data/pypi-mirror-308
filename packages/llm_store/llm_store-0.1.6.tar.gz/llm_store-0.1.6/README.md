# Feature

- LLM 配置读取远程存储
- Prompt 配置读取远程存储
- LLM 对话记录 存储到远程
- 远程存储: 支持 Baserow
- 支持使用 Jinja2 模板渲染 Prompt

# 默认使用模式
```python
from llm_store.gateway import LLMGateway
from llm_store.store.baserowstore import BaseRowStore
import os

## 初始化配置
store = BaseRowStore(
    api_host=os.environ.get("BASEROW_API_HOST", "localhost"),
    api_key=os.environ.get("BASEROW_API_KEY", ""),
    db_code="3",
    model_table_code="614",
    prompt_table_code="308",
    chat_log_table_code="309")
llm_gateway = LLMGateway(store)

## 渲染 Prompt 内容
prompt_code = "test_template"
prompt_record, messages = llm_gateway.render_prompt(prompt_code, {"topic": "科幻"})

## LLM 对话
chatCompletion, time_cost = llm_gateway.completions(prompt_record, messages)
print(chatCompletion,time_cost)

## 保存会话记录
trace_id = "1234567890"
log = llm_gateway.save_log(trace_id,prompt_record)
print(log)
```

# 轻量使用模式
说明: Prompt 不使用远程存储, 仅 LLM 配置, 对话记录存储到远程

```python
from llm_store.gateway import LLMGateway
from llm_store.store.baserowstore import BaseRowStore
import os

store = BaseRowStore(
    api_host=os.environ.get("BASEROW_API_HOST", "localhost"),
    api_key=os.environ.get("BASEROW_API_KEY", ""),
    db_code="3",
    model_table_code="614",
    prompt_table_code="308",
    chat_log_table_code="309")
llm_gateway = LLMGateway(store)

# 不使用远程 Prompt 模式
messages = [{"role": "system", "content": "今天星期几"}]

# -- 获取 模型信息
model_code = "litellm-us"
model_record = llm_gateway.get_model(model_code)

# -- 执行对话
chatCompletion = llm_gateway.completions(model_record, messages, trace_id="1234567890")
print(chatCompletion)
```