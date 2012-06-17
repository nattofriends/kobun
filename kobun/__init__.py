from .hypervisor import Hypervisor

def run(config):
    Hypervisor(config).run()

if __name__ == '__main__':
    run()

