def serialize_tool_calls(tool_calls):
    return [{
        "function":{
            "name": tool.funciton.name,
            "arguments": tool.funciton.arguments
        }
    }
    for tool in tool_calls
    ]