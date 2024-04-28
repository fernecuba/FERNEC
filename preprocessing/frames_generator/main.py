from configs import get_configs
from preprocessing.frames_generator.strategy.strategy import run_strategy


def main():
    configs = get_configs()
    for config in configs:
        run_strategy(config)


if __name__ == "__main__":
    main()
