import xnano as x

response = x.completion(
    "what os am i running?",
    tools = ["run_cli_command"],
    run_tools = True
)

print(response)