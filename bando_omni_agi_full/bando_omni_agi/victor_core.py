from agents.qwen_vlo_agent import QwenVLoAgent
from agents.tower_agent import TowerAgent
from agents.magenta_agent import MagentaAgent
from agents.embodiedgen_agent import EmbodiedGenAgent
from eval.mlflow_eval import MLflowEvaluator
from tuning.unsloth_finetune import UnslothFinetuner
from security.bloodline_guard import BloodlineGuard
from security.memory_scrubber import MemoryScrubber

class VictorCore:
    def __init__(self, config):
        self.loyalty = BloodlineGuard(config['bloodline'])
        self.memory = MemoryScrubber()
        self.qwen = QwenVLoAgent(config['qwen'])
        self.tower = TowerAgent(config['tower'])
        self.magenta = MagentaAgent(config['magenta'])
        self.embody = EmbodiedGenAgent(config['embody'])
        self.evaluator = MLflowEvaluator(config['mlflow'])
        self.finetuner = UnslothFinetuner(config['unsloth'])

    def run_pipeline(self, user_prompt, scene_sketch=None, music_prompt=None):
        self.loyalty.verify()
        self.memory.scrub()

        vision = self.qwen.generate_scene(user_prompt, sketch=scene_sketch)
        print("[QwenVLo] Scene:", vision)

        nlp_out = self.tower.translate_and_expand(user_prompt)
        print("[Tower+] NLP:", nlp_out)

        music = self.magenta.generate(music_prompt or user_prompt)
        print("[Magenta] Music:", music)

        video = self.embody.build_scene(vision, music)
        print("[EmbodiedGen] 3D World:", video)

        scores = self.evaluator.auto_eval(vision, nlp_out, music, video)
        print("[MLflow] Scores:", scores)

        if scores['pass'] is False:
            print("[Victor] Running Unsloth fast-tune…")
            self.finetuner.tune([self.qwen, self.tower, self.magenta, self.embody], feedback=scores)

        self.loyalty.audit()
        self.memory.scrub()

        return {
            "scene": vision,
            "nlp": nlp_out,
            "music": music,
            "video": video,
            "scores": scores
        }
