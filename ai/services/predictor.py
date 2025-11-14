from ai.models.model_manager import ModelManager

class AIPredictor:
    def __init__(self):
        self.model_manager = ModelManager()
        self.model_manager.load_model()

    def get_recommendation(self, usage_data):
        return self.model_manager.predict(usage_data)
