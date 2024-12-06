from __future__ import annotations

from typing import Callable, Union

from attrs import Factory, define, field

from griptape.artifacts import ImageArtifact, TextArtifact
from griptape.engines import PromptImageGenerationEngine
from griptape.tasks import BaseImageGenerationTask, BaseTask
from griptape.utils import J2


@define
class PromptImageGenerationTask(BaseImageGenerationTask):
    """Used to generate an image from a text prompt.

    Accepts prompt as input in one of the following formats:
    - template string
    - TextArtifact
    - Callable that returns a TextArtifact.

    Attributes:
        image_generation_engine: The engine used to generate the image.
        negative_rulesets: List of negatively-weighted rulesets applied to the text prompt, if supported by the driver.
        negative_rules: List of negatively-weighted rules applied to the text prompt, if supported by the driver.
        output_dir: If provided, the generated image will be written to disk in output_dir.
        output_file: If provided, the generated image will be written to disk as output_file.
    """

    DEFAULT_INPUT_TEMPLATE = "{{ args[0] }}"

    _input: Union[str, TextArtifact, Callable[[BaseTask], TextArtifact]] = field(
        default=DEFAULT_INPUT_TEMPLATE, alias="input"
    )
    image_generation_engine: PromptImageGenerationEngine = field(
        default=Factory(lambda: PromptImageGenerationEngine()),
        kw_only=True,
    )

    @property
    def input(self) -> TextArtifact:
        if isinstance(self._input, TextArtifact):
            return self._input
        elif isinstance(self._input, Callable):
            return self._input(self)
        else:
            return TextArtifact(J2().render_from_string(self._input, **self.full_context))

    @input.setter
    def input(self, value: TextArtifact) -> None:
        self._input = value

    def try_run(self) -> ImageArtifact:
        image_artifact = self.image_generation_engine.run(
            prompts=[self.input.to_text()],
            rulesets=self.rulesets,
            negative_rulesets=self.negative_rulesets,
        )

        if self.output_dir or self.output_file:
            self._write_to_file(image_artifact)

        return image_artifact
