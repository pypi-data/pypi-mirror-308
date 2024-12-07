import logging
from typing import List

from dria.client import Dria
from dria.models import Model
from dria.pipelines import PipelineConfig, Pipeline, StepConfig
from dria.pipelines.builder import PipelineBuilder
from .answer import AnswerStep
from .backstory import BackStoryStep
from .questions import QuestionStep
from .random_vars import RandomVarsStep

logger = logging.getLogger(__name__)


class QAPipeline:
    """
    A pipeline for generating QA pairs
    """

    def __init__(self, dria: Dria, config: PipelineConfig):
        self.pipeline_config: PipelineConfig = config or PipelineConfig()
        self.pipeline = PipelineBuilder(self.pipeline_config, dria)

    def build(
            self,
            simulation_description: str,
            num_samples: int,
            persona: str,
            chunks: List[str],
    ) -> Pipeline:
        self.pipeline.input(simulation_description=simulation_description)
        (
            self.pipeline
            << RandomVarsStep(num_of_samples=num_samples, config=StepConfig(max_tokens=1500))
            .set_models([Model.OPENAI, Model.GEMINI]).custom()
            << BackStoryStep(chunks=chunks, config=StepConfig())
            .set_models([Model.OPENAI, Model.GEMINI]).custom()
            << QuestionStep(persona=persona, config=StepConfig())
            .set_models([Model.OPENAI, Model.OLLAMA])
            << AnswerStep(config=StepConfig()).set_models([Model.OPENAI, Model.OLLAMA])
        )
        return self.pipeline.build()
