"""Small smoke check for the guarded runtime path."""
from autonomous_core.runtime_entrypoint import RuntimeEntrypoint

def main():
    runtime = RuntimeEntrypoint(lambda action, payload: {"action": action, "payload": payload})
    result = runtime.run("inspect", {"smoke": True}, critical=False)
    assert result["status"] == "executed"
    assert result["result"]["action"] == "inspect"
    return result

if __name__ == "__main__":
    print(main())
