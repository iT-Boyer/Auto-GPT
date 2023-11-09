def parse_agent_name_and_goals(name_and_goals: dict) -> str:
    parsed_response = f"助手名称: {name_and_goals['agent_name']}\n"
    parsed_response += f"助手角色: {name_and_goals['agent_role']}\n"
    parsed_response += "助手目标:\n"
    for i, goal in enumerate(name_and_goals["agent_goals"]):
        parsed_response += f"{i+1}. {goal}\n"
    return parsed_response


def parse_agent_plan(plan: dict) -> str:
    parsed_response = "助手计划:\n"
    for i, task in enumerate(plan["task_list"]):
        parsed_response += f"{i+1}. {task['objective']}\n"
        parsed_response += f"任务类型: {task['type']}  "
        parsed_response += f"优先级: {task['priority']}\n"
        parsed_response += "准备好条件:\n"
        for j, criteria in enumerate(task["ready_criteria"]):
            parsed_response += f"    {j+1}. {criteria}\n"
        parsed_response += "验收标准:\n"
        for j, criteria in enumerate(task["acceptance_criteria"]):
            parsed_response += f"    {j+1}. {criteria}\n"
        parsed_response += "\n"

    return parsed_response


def parse_next_ability(current_task, next_ability: dict) -> str:
    parsed_response = f"当前任务: {current_task.objective}\n"
    ability_args = ", ".join(
        f"{k}={v}" for k, v in next_ability["ability_arguments"].items()
    )
    parsed_response += f"下一个技能: {next_ability['next_ability']}({ability_args})\n"
    parsed_response += f"愿景期望: {next_ability['motivation']}\n"
    parsed_response += f"自我批评: {next_ability['self_criticism']}\n"
    parsed_response += f"推演过程: {next_ability['reasoning']}\n"
    return parsed_response


def parse_ability_result(ability_result) -> str:
    parsed_response = f"技能: {ability_result['ability_name']}\n"
    parsed_response += f"技能要领: {ability_result['ability_args']}\n"
    parsed_response += f"技能成果: {ability_result['success']}\n"
    parsed_response += f"信息: {ability_result['message']}\n"
    parsed_response += f"数据: {ability_result['new_knowledge']}\n"
    return parsed_response
