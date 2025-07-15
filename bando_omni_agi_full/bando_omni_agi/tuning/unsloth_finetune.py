class UnslothFinetuner:
    def __init__(self, config):
        self.config = config

    def tune(self, agents, feedback):
        # Iterate fast finetune on underperforming agents
        print(f"Unsloth tuning on: {[agent.__class__.__name__ for agent in agents]} w/feedback: {feedback}")
