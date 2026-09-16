from autonomous_core.supervisor import AutonomousSupervisor


if __name__ == "__main__":
    supervisor = AutonomousSupervisor()
    supervisor.set_desired_state("running")
    supervisor.run_forever()
