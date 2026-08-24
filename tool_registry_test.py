from tool_registry import TOOL_REGISTRY


for tool_name, tool_config in TOOL_REGISTRY.items():
    tool_function = tool_config["function"]
    argument_name = tool_config["argument"]

    print(
        tool_name,
        "->",
        tool_function.__name__,
        "| argument:",
        argument_name
    )