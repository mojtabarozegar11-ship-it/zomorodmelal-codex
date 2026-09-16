from __future__ import annotations

import ast
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .access_manager import AccessManager
from .activation_gate import ActivationGate
from .agent_factory import AgentFactory


class MasterCore:
    """Master Agent kernel for the complete 15-generation autonomous lifecycle.

    The core owns observation, diagnosis, goal selection, delegation, safe
    execution planning, verification, learning and evolutionary progression.
    It never authorizes real-world actions; those remain owner-gated.
    """

    VERSION = "15.0.0"
    MAX_GENERATION = 15
    PHASES = [
        "observe", "diagnose", "prioritize", "delegate", "plan", "execute",
        "test", "repair", "verify", "learn", "evolve", "next_goal",
    ]
    GENERATIONS = {
        1: "observation",
        2: "diagnosis",
        3: "goal_prioritization",
        4: "agent_delegation",
        5: "planning",
        6: "sandbox_execution",
        7: "testing",
        8: "self_repair",
        9: "verification",
        10: "learning",
        11: "evolution",
        12: "continuous_goals",
        13: "multi_agent_coordination",
        14: "resilience_and_rollback",
        15: "closed_loop_master_agent",
    }
    GOAL_ACCESS_RULES = {
        "web_research": ("research", "تحقیق", "جستجو", "خبر", "بازار", "اطلاعات"),
        "github_repo": ("github", "repository", "repo", "کد", "code", "مخزن"),
        "telegram_bot": ("telegram", "تلگرام", "bot", "ربات"),
        "hosting": ("deploy", "deployment", "hosting", "publish", "استقرار", "هاست", "انتشار"),
        "payments": ("payment", "payments", "پرداخت", "فروش", "درآمد", "تراکنش"),
        "email": ("email", "e-mail", "ایمیل"),
        "calendar": ("calendar", "schedule", "تقویم", "زمانبندی"),
        "secrets": ("secret", "secrets", "credential", "credentials", "کلید api", "رمز"),
        "browser_automation": ("browser", "automation", "اتوماسیون مرورگر", "مرورگر"),
    }
    REQUIRED_CAPABILITIES = {
        "planning", "research", "memory", "knowledge_management", "evaluation",
        "sandbox_execution", "automated_testing", "rollback", "owner_approval",
        "execution_control", "orchestration", "agent_generation", "evolution",
    }

    def __init__(self, root=None):
        self.root = os.path.abspath(root or os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.root, "data")
        self.sandbox_dir = os.path.join(self.root, "sandbox", "autonomous_workspace")
        self.state_file = os.path.join(self.data_dir, "master_core_state.json")
        self.mission_file = os.path.join(self.data_dir, "master_mission_queue.json")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.sandbox_dir, exist_ok=True)
        self.access_manager = AccessManager(self.root)
        self.activation_gate = ActivationGate(self.root, self.access_manager)
        self.agent_factory = AgentFactory(self.root)
        self.state = self._load_state()

    def _defaults(self):
        return {"version": self.VERSION, "cycles": 0, "generation": 1,
                "phase": "observe", "goals": [], "agents": [], "capabilities": [],
                "proposals": [], "access_requests": [], "activation_checks": [],
                "mission_history": [], "learning": [], "failures": [],
                "last_cycle": None, "last_decision": None, "last_result": None}

    def _normalize_state(self, state):
        defaults = self._defaults()
        if not isinstance(state, dict): state = {}
        for key, value in defaults.items():
            if key not in state or state[key] is None:
                state[key] = value.copy() if isinstance(value, list) else value
        state["version"] = self.VERSION
        try: state["generation"] = max(1, min(self.MAX_GENERATION, int(state.get("generation", 1))))
        except (TypeError, ValueError): state["generation"] = 1
        if state.get("phase") not in self.PHASES: state["phase"] = "observe"
        return state

    def _load_state(self):
        if not os.path.exists(self.state_file):
            state = self._defaults(); self._save_state(state); return state
        try:
            with open(self.state_file, "r", encoding="utf-8") as f: return self._normalize_state(json.load(f))
        except Exception: return self._defaults()

    def _save_state(self, state=None):
        if state is not None: self.state = self._normalize_state(state)
        else: self.state = self._normalize_state(self.state)
        tmp = self.state_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f: json.dump(self.state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.state_file)

    def _write_json(self, path, value):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f: json.dump(value, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    def set_goal(self, goal):
        goal = str(goal or "").strip()
        if not goal: raise ValueError("goal is required")
        for item in reversed(self.state["goals"]):
            if item.get("text") == goal and item.get("status") == "active": return item
        item = {"id": max((int(x.get("id", 0)) for x in self.state["goals"]), default=0) + 1,
                "text": goal, "status": "active", "created_at": datetime.now(timezone.utc).isoformat()}
        self.state["goals"].append(item); self._save_state(); return item

    def discover_project(self):
        files = []; ignored = {".git", "__pycache__", ".venv", "venv", "node_modules"}
        for current, dirs, names in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for name in names: files.append(os.path.relpath(os.path.join(current, name), self.root))
        return files

    def audit_python(self):
        results = []
        for relative in self.discover_project():
            if not relative.endswith(".py"): continue
            result = {"file": relative, "syntax_ok": False, "error": None}
            try:
                with open(os.path.join(self.root, relative), "r", encoding="utf-8") as f: ast.parse(f.read())
                result["syntax_ok"] = True
            except Exception as e: result["error"] = str(e)
            results.append(result)
        return results

    def discover_capabilities(self):
        capabilities = set()
        mapping = {"research": "research", "agent_factory": "agent_generation", "factory": "agent_generation",
                   "sandbox": "sandbox_execution", "testing": "automated_testing", "evolution": "evolution",
                   "versioning": "rollback", "approval": "owner_approval", "execution": "execution_control",
                   "orchestrator": "orchestration", "access": "access_management", "knowledge": "knowledge_management",
                   "memory": "memory", "planner": "planning", "evaluation": "evaluation"}
        for relative in self.discover_project():
            for part in relative.replace("\\", "/").split("/"):
                if part in mapping: capabilities.add(mapping[part])
        self.state["capabilities"] = sorted(capabilities); return sorted(capabilities)

    def discover_agents(self):
        factory = getattr(self, "agent_factory", None)
        agents = factory.list_agents() if factory else []
        agent_dir = os.path.join(self.root, "agents")
        if os.path.isdir(agent_dir):
            known = {x.get("name") for x in agents}
            for name in os.listdir(agent_dir):
                if name.endswith(".py") and name[:-3] not in known:
                    agents.append({"name": name[:-3], "source": "agents", "status": "discovered"})
        self.state["agents"] = agents; return agents

    def ensure_agents_for_mission(self, mission):
        factory = getattr(self, "agent_factory", None)
        if not factory: return []
        roles = mission.get("roles", ["general"])
        return [factory.ensure_agent(role, mission.get("id", "")) for role in roles]

    def analyze_gaps(self): return sorted(self.REQUIRED_CAPABILITIES - set(self.state.get("capabilities", [])))

    def design_agents(self, missing):
        templates = {"planning": ("StrategicPlannerAgent", "تحلیل هدف و طراحی برنامه"),
                     "research": ("ResearchAgent", "تحقیق و جمع‌آوری دانش"),
                     "sandbox_execution": ("SandboxAgent", "ساخت و آزمایش امن"),
                     "automated_testing": ("TestingAgent", "تست و تشخیص شکست"),
                     "agent_generation": ("AgentFactoryAgent", "طراحی و تولید زیرایجنت"),
                     "evolution": ("EvolutionAgent", "طراحی نسل جدید"),
                     "orchestration": ("OrchestratorAgent", "هماهنگی زیرایجنت‌ها")}
        return [{"name": templates[c][0], "purpose": templates[c][1], "capability": c,
                 "status": "design_only", "owner_approval_required": True} for c in missing if c in templates]

    def discover_access_requirements(self):
        manager = getattr(self, "access_manager", None)
        requirements = manager.discover(self.state.get("capabilities", [])) if manager else []
        self.state["access_requests"] = requirements; return requirements

    def required_access_for_goal(self, goal):
        text = str(goal or "").strip().lower()
        return sorted({cap for cap, keys in self.GOAL_ACCESS_RULES.items() if any(k.lower() in text for k in keys)})

    def request_goal_access(self, goal):
        manager = getattr(self, "access_manager", None)
        if not manager: return []
        requests = [manager.request(cap, goal) for cap in self.required_access_for_goal(goal)]
        self.state["access_requests"] = manager.status()["requests"]; return requests

    def check_activation(self, request_id, capability, scope="minimum_required"):
        decision = self.activation_gate.authorize(request_id, capability, scope)
        self.state["activation_checks"].append({**decision, "checked_at": datetime.now(timezone.utc).isoformat()})
        self._save_state(); return decision

    def create_proposals(self, missing, designs):
        proposals = [{"type": "capability_upgrade", "capability": c, "status": "proposal_only", "owner_approval_required": True} for c in missing]
        proposals += [{"type": "agent_generation", "agent": d["name"], "capability": d["capability"], "status": "proposal_only", "owner_approval_required": True} for d in designs]
        self.state["proposals"] = proposals; return proposals

    def choose_next_mission(self, goal, audit, missing):
        failures = [x for x in audit if not x["syntax_ok"]]
        if failures: return {"id": "quality.syntax_repair", "priority": 100, "roles": ["engineering", "testing"], "reason": "syntax failures", "failure_count": len(failures)}
        if goal and any(k in goal.lower() for k in ("repair", "اصلاح", "تعمیر")):
            return {"id": "quality.repair_and_retest", "priority": 95, "roles": ["engineering", "testing"], "reason": "explicit repair objective"}
        if missing: return {"id": "system.capability_completion", "priority": 90, "roles": ["engineering", "general"], "reason": "capability gap detected", "missing": missing}
        if not self.state.get("agents"): return {"id": "agent.ecosystem_bootstrap", "priority": 85, "roles": ["general"], "reason": "subordinate ecosystem missing"}
        return {"id": "continuous.improvement", "priority": 50, "roles": ["general", "testing"], "reason": "continue autonomous improvement"}

    def plan_mission(self, mission):
        return {"mission_id": mission["id"], "steps": ["prepare_sandbox", "delegate", "execute_safe_actions", "test", "verify", "record_learning"],
                "safe_execution": True, "real_world_execution": False, "owner_approval_required": True}

    def _learn(self, mission, success, evidence=None):
        event = {"timestamp": datetime.now(timezone.utc).isoformat(), "mission": mission["id"], "success": bool(success),
                 "generation": self.state["generation"], "evidence": evidence or {}}
        self.state["learning"].append(event); self.state["learning"] = self.state["learning"][-200:]
        if success and self.state["generation"] < self.MAX_GENERATION: self.state["generation"] += 1
        return event

    def autonomous_step(self, goal=None, test_passed=None):
        """Perform one complete decision step and return an executable-safe plan.

        The actual trusted test/execution engine may supply `test_passed` on a
        later step. The core never treats a missing test result as success.
        """
        result = self.run_cycle(goal=goal, test_passed=test_passed)
        return result

    def run_cycle(self, goal=None, test_passed=None):
        self.state = self._normalize_state(self.state)
        if goal: self.set_goal(goal)
        active_goal = goal or (self.state["goals"][-1]["text"] if self.state["goals"] else None)
        self.state["cycles"] += 1
        self.state["phase"] = "observe"
        audit = self.audit_python()
        capabilities = self.discover_capabilities()
        agents = self.discover_agents()
        self.state["phase"] = "diagnose"
        missing = self.analyze_gaps()
        designs = self.design_agents(missing)
        access = self.discover_access_requirements()
        goal_access = self.request_goal_access(active_goal)
        self.state["phase"] = "prioritize"
        mission = self.choose_next_mission(active_goal, audit, missing)
        self.state["phase"] = "delegate"
        delegated = self.ensure_agents_for_mission(mission)
        self.state["phase"] = "plan"
        plan = self.plan_mission(mission)
        self.state["phase"] = "execute"
        execution = {"status": "sandbox_planned", "safe": True, "real_world_action": False}
        self.state["phase"] = "test"
        test_state = "pending" if test_passed is None else ("passed" if test_passed else "failed")
        self.state["phase"] = "repair" if test_passed is False else "verify"
        if test_passed is False:
            self.state["failures"].append({"mission": mission["id"], "timestamp": datetime.now(timezone.utc).isoformat()})
            self.state["failures"] = self.state["failures"][-100:]
        success = test_passed is True
        self.state["phase"] = "learn"
        learning = self._learn(mission, success, {"test": test_state})
        self.state["phase"] = "evolve"
        if success and self.state["generation"] < self.MAX_GENERATION: self.state["generation"] += 1
        self.state["phase"] = "next_goal"
        self.state["last_decision"] = mission
        self.state["mission_history"].append({"cycle": self.state["cycles"], **mission, "test": test_state})
        self.state["mission_history"] = self.state["mission_history"][-200:]
        self.state["last_cycle"] = datetime.now(timezone.utc).isoformat()
        self.state["last_result"] = {"mission": mission["id"], "test": test_state, "generation": self.state["generation"]}
        self._save_state()
        queue = {"current": mission, "plan": plan, "delegated_agents": delegated, "status": "ready_for_safe_execution",
                 "owner_approval_required": True, "real_world_changes_allowed": False, "sandbox_only": True,
                 "next_generation": self.state["generation"], "updated_at": datetime.now(timezone.utc).isoformat()}
        self._write_json(self.mission_file, queue)
        return {"version": self.VERSION, "cycle": self.state["cycles"], "generation": self.state["generation"],
                "phase": self.state["phase"], "goal": active_goal, "files": len(self.discover_project()),
                "python_files": len(audit), "syntax_errors": [x for x in audit if not x["syntax_ok"]],
                "capabilities": capabilities, "missing_capabilities": missing, "agents": agents,
                "delegated_agents": delegated, "new_agent_designs": designs, "access_requirements": access,
                "goal_access_requirements": [x["capability"] for x in goal_access], "proposals": self.create_proposals(missing, designs),
                "mission": mission, "plan": plan, "execution": execution, "test": test_state, "learning": learning,
                "owner_approval_required": True, "real_changes_allowed": False, "sandbox_only": True}

    def status(self):
        self.state = self._normalize_state(self.state)
        return {"master_core": True, "version": self.VERSION, "max_generation": self.MAX_GENERATION,
                "generation": self.state.get("generation", 1), "phase": self.state.get("phase", "observe"),
                "cycles": self.state.get("cycles", 0), "goals": len(self.state.get("goals", [])),
                "agents": len(self.state.get("agents", [])), "capabilities": len(self.state.get("capabilities", [])),
                "missions": len(self.state.get("mission_history", [])), "learning_events": len(self.state.get("learning", [])),
                "failures": len(self.state.get("failures", [])), "owner_approval_required": True,
                "real_changes_allowed": False, "sandbox_only": True, "generations": self.GENERATIONS}
