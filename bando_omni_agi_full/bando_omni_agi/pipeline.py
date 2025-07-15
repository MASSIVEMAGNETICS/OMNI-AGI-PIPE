if __name__ == "__main__":
    import yaml
    from victor_core import VictorCore

    config = yaml.safe_load(open("config.yaml"))
    victor = VictorCore(config)

    result = victor.run_pipeline(
        user_prompt="Create a dark futuristic cityscape with a glowing clock, generate an epic trap melody and a 3D music video."
    )
    print(result)
