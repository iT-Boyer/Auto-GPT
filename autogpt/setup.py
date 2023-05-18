"""Set up the AI and its goals"""
import re

from colorama import Fore, Style
from jinja2 import Template

from autogpt import utils
from autogpt.config import Config
from autogpt.config.ai_config import AIConfig
from autogpt.llm import create_chat_completion
from autogpt.logs import logger
from autogpt.prompts.default_prompts import (
    DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC,
    DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC,
    DEFAULT_USER_DESIRE_PROMPT,
)

CFG = Config()


def prompt_user() -> AIConfig:
    """Prompt the user for input

    Returns:
        AIConfig: The AIConfig object tailored to the user's input
    """
    ai_name = ""
    ai_config = None

    # Construct the prompt
    logger.typewriter_log(
        "自动模式:",
        Fore.GREEN,
        "输入 '--help' 查看帮助文档",
        speak_text=True,
    )

    # Get user desire
    logger.typewriter_log(
        "制作助手:",
        Fore.GREEN,
        "输入 '--manual' 切换手动模式",
        speak_text=True,
    )

    user_desire = utils.clean_input(f"{Fore.LIGHTBLUE_EX}投喂需求{Style.RESET_ALL}: ")

    if user_desire == "":
        user_desire = DEFAULT_USER_DESIRE_PROMPT  # Default prompt

    # If user desire contains "--manual"
    if "--manual" in user_desire:
        logger.typewriter_log(
            "启动手动模式",
            Fore.GREEN,
            speak_text=True,
        )
        return generate_aiconfig_manual()

    else:
        try:
            return generate_aiconfig_automatic(user_desire)
        except Exception as e:
            logger.typewriter_log(
                "助手制作失败，自动模式无法处理您的需求!",
                Fore.RED,
                "启动手动模式。",
                speak_text=True,
            )

            return generate_aiconfig_manual()


def generate_aiconfig_manual() -> AIConfig:
    """
    Interactively create an AI configuration by prompting the user to provide the name, role, and goals of the AI.

    This function guides the user through a series of prompts to collect the necessary information to create
    an AIConfig object. The user will be asked to provide a name and role for the AI, as well as up to five
    goals. If the user does not provide a value for any of the fields, default values will be used.

    Returns:
        AIConfig: An AIConfig object containing the user-defined or default AI name, role, and goals.
    """

    # Manual Setup Intro
    logger.typewriter_log(
        "制作说明:",
        Fore.GREEN,
        "请在下面引导下，输入助手名称，角色职能和目标。或回车启用默认助手。",
        speak_text=True,
    )

    # Get AI Name from User
    logger.typewriter_log("命名规范:", Fore.GREEN, "例如, '健身达人'")
    ai_name = utils.clean_input("助手名称: ")
    if ai_name == "":
        ai_name = "企业家-GPT"

    logger.typewriter_log(
        f"{ai_name} 嗨!", Fore.LIGHTBLUE_EX, "随时为您服务。", speak_text=True
    )

    # Get AI Role from User
    logger.typewriter_log(
        "角色说明:",
        Fore.GREEN,
        "为助手的设计一个角色，撰写角色的职能和使命宣言，例如：'这个助手被设计成能够自主发展和经营企业，唯一的目标就是帮你增加净资产。'",
    )
    ai_role = utils.clean_input(f"{ai_name}的角色职能: ")
    if ai_role == "":
        ai_role = "这个助手被设计成能够自主发展和经营企业，唯一的目标就是帮你增加净资产。"

    # Enter up to 5 goals for the AI
    logger.typewriter_log(
        "目标说明:",
        Fore.GREEN,
        "为助手添加职业目标,例如: \n 增加收益，抖音涨粉，自主开发和管理多个业务",
    )
    logger.info("不输入加载默认设置，不要输入任何内容代表目标设置完成。")
    ai_goals = []
    for i in range(5):
        ai_goal = utils.clean_input(f"{Fore.LIGHTBLUE_EX}目标{Style.RESET_ALL} {i+1}: ")
        if ai_goal == "":
            break
        ai_goals.append(ai_goal)
    if not ai_goals:
        ai_goals = [
            "增加收入",
            "增加用户",
            "自主开发和管理多个业务",
        ]

    # Get API Budget from User
    logger.typewriter_log(
        "API预算: ",
        Fore.GREEN,
        "例如: $1.50",
    )
    logger.info("不设置，即没有上限")
    api_budget_input = utils.clean_input(f"{Fore.LIGHTBLUE_EX}预算{Style.RESET_ALL}: $")
    if api_budget_input == "":
        api_budget = 0.0
    else:
        try:
            api_budget = float(api_budget_input.replace("$", ""))
        except ValueError:
            logger.typewriter_log("无效的预算输入。即没有上限。", Fore.RED)
            api_budget = 0.0

    return AIConfig(ai_name, ai_role, ai_goals, api_budget)


def generate_aiconfig_automatic(user_prompt) -> AIConfig:
    """Generates an AIConfig object from the given string.

    Returns:
    AIConfig: The AIConfig object tailored to the user's input
    """

    system_prompt = DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC
    prompt_ai_config_automatic = Template(
        DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC
    ).render(user_prompt=user_prompt)
    # Call LLM with the string as user input
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt_ai_config_automatic,
        },
    ]
    output = create_chat_completion(messages, CFG.fast_llm_model)

    # Debug LLM Output
    logger.debug(f"自动生成的AI配置: {output}")

    # Parse the output
    ai_name = re.search(r"Name(?:\s*):(?:\s*)(.*)", output, re.IGNORECASE).group(1)
    ai_role = (
        re.search(
            r"Description(?:\s*):(?:\s*)(.*?)(?:(?:\n)|Goals)",
            output,
            re.IGNORECASE | re.DOTALL,
        )
        .group(1)
        .strip()
    )
    ai_goals = re.findall(r"(?<=\n)-\s*(.*)", output)
    api_budget = 0.0  # TODO: parse api budget using a regular expression

    return AIConfig(ai_name, ai_role, ai_goals, api_budget)
