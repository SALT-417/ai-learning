from tool_registry import TOOL_REGISTRY


for tool_name, tool_config in TOOL_REGISTRY.items():
    tool_function = tool_config["function"]
    requires_minutes = tool_config[
        "requires_minutes"
    ]

    print(
        tool_name,
        "->",
        tool_function.__name__,
        "| requires_minutes:",
        requires_minutes
    )