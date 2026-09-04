def serialize_tool_calls(tool_calls):
    return [{
        "function":{
            "name": tool.function.name,
            "arguments": tool.function.arguments
        }
    }
    for tool in tool_calls
    ]