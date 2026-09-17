from .serializers import AgentRequestSerializer


def agent_execute(request_data):
    serializer = AgentRequestSerializer(data=request_data)
    if not serializer.is_valid():
        return {"status": "error", "details": serializer.errors}

    return {
        "status": "accepted",
        "goal": serializer.validated_data.get("goal"),
        "message": "Request prepared for Agent Bridge"
    }
