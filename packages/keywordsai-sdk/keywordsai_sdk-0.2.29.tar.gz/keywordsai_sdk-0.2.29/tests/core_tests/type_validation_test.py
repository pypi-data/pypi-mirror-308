from keywordsai_sdk.keywordsai_types.param_types import KeywordsAITextLogParams

class TestTypeValidation:
    def __init__(self):
        self.ttft = 0.1
        self.generation_time = 0.2



to_validate= TestTypeValidation()
params = KeywordsAITextLogParams(**to_validate.__dict__)
params