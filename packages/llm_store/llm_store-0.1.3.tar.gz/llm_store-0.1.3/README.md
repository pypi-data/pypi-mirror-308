# 初始化配置
store = BaseRowStore(
    api_host="...",
    api_key="...",
    db_code="3",
    model_table_code="614",
    prompt_table_code="308",
    chat_log_table_code="309")
llm_gateway = LLMGateway(store)

# 渲染 Prompt 内容
prompt_code = "test_template"
prompt_record, messages = llm_gateway.render_prompt(prompt_code, {"topic": "科幻"})

# LLM 对话
chatCompletion, time_cost = llm_gateway.completions(prompt_record, messages)
print(chatCompletion,time_cost)

# 保存会话记录
trace_id = "1234567890"
log = llm_gateway.save_log(trace_id,prompt_record)
print(log)
