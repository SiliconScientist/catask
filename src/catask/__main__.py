from catask.config import get_config


def main():
    cfg = get_config()
    print(f"Random seed is set to: {cfg.seed}")


if __name__ == "__main__":
    main()
