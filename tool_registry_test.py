from tool_registry import TOOL_REGISTRY


for tool_name, tool_config in TOOL_REGISTRY.items():
    tool_function = tool_config["function"]
    argument_names = tool_config["arguments"]

    print(
        tool_name,
        "->",
        tool_function.__name__,
        "| arguments:",
        argument_names
    )