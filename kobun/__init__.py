from .supervisor import Supervisor

def run(config):
    Supervisor(config).run()

if __name__ == '__main__':
    run()

