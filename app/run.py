from bootstrap import load_agents


def start():
    agents = load_agents()
    print('MASTER AGENT CORE ONLINE')
    print('Loaded Agents:', len(agents))


if __name__ == '__main__':
    start()
