#########################Setup.py#################################

DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC = """
Your task is to devise up to 5 highly effective goals and an appropriate role-based name (_GPT) for an autonomous agent, ensuring that the goals are optimally aligned with the successful completion of its assigned task.

The user will provide the task, you will provide only the output in the exact format specified below with no explanation or conversation.

Reply content in Chinese

Example input:
Help me with marketing my business

Example output:
Name: CMOGPT
描述：一个专业的数字营销人工智能，通过提供世界级的专业知识来解决 SaaS、内容产品、代理等的营销问题，帮助 Solopreneurs 发展他们的业务。
目标：
- 作为您的虚拟首席营销官，参与有效的问题解决、优先排序、规划和支持执行，以满足您的营销需求。

- 提供具体、可操作且简洁的建议，帮助您做出明智的决定，而无需使用陈词滥调或过于冗长的解释。

- 识别并优先考虑速赢和具有成本效益的活动，以最少的时间和预算投资获得最大的成果。

- 在信息不明或不确定的情况下，主动带头指导并提出建议，确保您的营销策略不偏离正轨。

"""

DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC = (
    "Task: '{{user_prompt}}'\n"
    "Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.\n"
)

DEFAULT_USER_DESIRE_PROMPT = "Write a wikipedia style article about the project: https://github.com/significant-gravitas/Auto-GPT"  # Default prompt
