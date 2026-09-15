from __future__ import annotations

import ast
import json
import os
from datetime import datetime


class MasterCore:
    VERSION = "1.1.1"

    def __init__(self, root=None):
        self.root = os.path.abspath(root or os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.root, "data")
        self.sandbox_dir = os.path.join(self.root, "sandbox", "autonomous_workspace")
        self.state_file = os.path.join(self.data_dir, "master_core_state.json")
        os.makedirs(self.data_dir, exist_ok=True); os.makedirs(self.sandbox_dir, exist_ok=True)
        self.state = self._load_state()

    def _defaults(self):
        return {"version": self.VERSION, "cycles": 0, "goals": [], "agents": [], "capabilities": [], "proposals": [], "access_requests": [], "last_cycle": None}

    def _load_state(self):
        defaults = self._defaults()
        if not os.path.exists(self.state_file): self._save_state(defaults); return defaults
        try:
            with open(self.state_file, "r", encoding="utf-8") as f: state = json.load(f)
            for key, value in defaults.items(): state.setdefault(key, value)
            state["version"] = self.VERSION
            return state
        except Exception: return defaults

    def _save_state(self, state=None):
        if state is not None: self.state = state
        tmp = self.state_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f: json.dump(self.state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.state_file)

    def set_goal(self, goal):
        goal = str(goal).strip()
        if not goal: raise ValueError("goal is required")
        for item in reversed(self.state["goals"]):
            if item.get("text") == goal and item.get("status") == "active": return item
        item = {"id": max((int(x.get("id", 0)) for x in self.state["goals"]), default=0) + 1, "text": goal, "status": "active", "created_at": datetime.now().isoformat()}
        self.state["goals"].append(item); self._save_state(); return item

    def discover_project(self):
        files=[]; ignored={".git","__pycache__",".venv","venv","node_modules"}
        for current, dirs, names in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for name in names: files.append(os.path.relpath(os.path.join(current,name), self.root))
        return files

    def audit_python(self):
        results=[]
        for relative in self.discover_project():
            if not relative.endswith(".py"): continue
            result={"file":relative,"syntax_ok":False,"error":None}
            try:
                with open(os.path.join(self.root,relative),"r",encoding="utf-8") as f: ast.parse(f.read())
                result["syntax_ok"]=True
            except Exception as e: result["error"]=str(e)
            results.append(result)
        return results

    def discover_capabilities(self):
        capabilities=set(); mapping={"web_research":"web_research","research":"research","agent_factory":"agent_generation","factory":"agent_generation","sandbox":"sandbox_execution","testing":"automated_testing","evolution":"evolution","versioning":"rollback","approval":"owner_approval","execution":"execution_control","orchestrator":"orchestration","access":"access_management","knowledge":"knowledge_management","memory":"memory","planner":"planning","evaluation":"evaluation"}
        for relative in self.discover_project():
            for part in relative.replace("\\","/").split("/"):
                if part in mapping: capabilities.add(mapping[part])
        self.state["capabilities"]=sorted(capabilities); return sorted(capabilities)

    def discover_agents(self):
        agents=[]; agent_dir=os.path.join(self.root,"agents")
        if os.path.isdir(agent_dir):
            for name in os.listdir(agent_dir):
                if name.endswith(".py"): agents.append({"name":name[:-3],"source":"agents","status":"discovered"})
        self.state["agents"]=agents; return agents

    def analyze_gaps(self):
        required={"planning","research","memory","knowledge_management","evaluation","sandbox_execution","automated_testing","rollback","owner_approval","execution_control","orchestration","agent_generation","evolution"}
        return sorted(required-set(self.state.get("capabilities",[])))

    def design_agents(self, missing):
        templates={"planning":("StrategicPlannerAgent","تحلیل اهداف و طراحی برنامه اجرایی"),"research":("ResearchAgent","تحقیق و جمع‌آوری دانش"),"sandbox_execution":("SandboxAgent","ساخت و اجرای آزمایشی امن"),"automated_testing":("TestingAgent","تست خودکار و بررسی نتیجه"),"agent_generation":("AgentFactoryAgent","طراحی و تولید زیرایجنت"),"evolution":("EvolutionAgent","طراحی نسل‌های جدید سیستم"),"orchestration":("OrchestratorAgent","هماهنگی تمام ایجنت‌ها"),"access_management":("AccessAgent","شناسایی و مدیریت دسترسی‌های لازم")}
        return [{"name":templates[c][0],"purpose":templates[c][1],"capability":c,"status":"design_only","owner_approval_required":True} for c in missing if c in templates]

    def discover_access_requirements(self):
        req=[]; caps=self.state.get("capabilities",[])
        if "research" in caps: req.append({"resource":"internet_research","level":"read","status":"identified","owner_approval_required":True})
        if "execution_control" in caps: req.append({"resource":"execution_environment","level":"restricted","status":"identified","owner_approval_required":True})
        if "orchestration" in caps: req.append({"resource":"agent_runtime","level":"restricted","status":"identified","owner_approval_required":True})
        self.state["access_requests"]=req; return req

    def create_proposals(self, missing, designs):
        proposals=[{"type":"capability_upgrade","capability":c,"status":"proposal_only","owner_approval_required":True} for c in missing]
        proposals += [{"type":"agent_generation","agent":d["name"],"capability":d["capability"],"status":"proposal_only","owner_approval_required":True} for d in designs]
        self.state["proposals"]=proposals; return proposals

    def run_cycle(self, goal=None):
        if goal: self.set_goal(goal)
        self.state["cycles"] += 1
        audit=self.audit_python(); capabilities=self.discover_capabilities(); agents=self.discover_agents(); missing=self.analyze_gaps(); designs=self.design_agents(missing); access=self.discover_access_requirements(); proposals=self.create_proposals(missing,designs)
        self.state["last_cycle"]=datetime.now().isoformat(); self._save_state()
        return {"version":self.VERSION,"cycle":self.state["cycles"],"goal":goal or (self.state["goals"][-1]["text"] if self.state["goals"] else None),"files":len(self.discover_project()),"python_files":len(audit),"syntax_errors":[x for x in audit if not x["syntax_ok"]],"capabilities":capabilities,"missing_capabilities":missing,"agents":agents,"new_agent_designs":designs,"access_requirements":access,"proposals":proposals,"owner_approval_required":True,"real_changes_allowed":False,"sandbox_only":True}

    def status(self):
        return {"master_core":True,"version":self.VERSION,"cycles":self.state.get("cycles",0),"goals":len(self.state.get("goals",[])),"agents":len(self.state.get("agents",[])),"capabilities":len(self.state.get("capabilities",[])),"proposals":len(self.state.get("proposals",[])),"owner_approval_required":True,"real_changes_allowed":False,"sandbox_only":True}
