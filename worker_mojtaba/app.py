from worker_mojtaba.core.brain import CoreBrain, Task
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.core.planner import Planner
from worker_mojtaba.core.router import Router

def run(request:str)->dict:
    brain, memory, planner, router = CoreBrain(), MemoryStore(), Planner(), Router()
    plan = planner.make_plan(request)
    route = router.route("text_model", ["text_model","video","image","audio"])
    result = brain.plan(Task(request, {}))
    memory.remember_short(result)
    result.update({"plan":plan,"route":route})
    return result

if __name__=="__main__": print(run("سلام"))
