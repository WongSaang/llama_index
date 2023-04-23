"""Default query for GPTEmptyIndex."""
from typing import Any, List, Optional

from gpt_index.data_structs.data_structs_v2 import EmptyIndex
from gpt_index.indices.query.base import BaseGPTIndexQuery
from gpt_index.data_structs.node_v2 import NodeWithScore
from gpt_index.indices.query.schema import QueryBundle
from gpt_index.indices.response.type import ResponseMode
from gpt_index.prompts.default_prompts import DEFAULT_SIMPLE_INPUT_PROMPT
from gpt_index.prompts.prompts import SimpleInputPrompt
from gpt_index.response.schema import (
    RESPONSE_TYPE,
    Response,
    StreamingResponse,
)


class GPTEmptyIndexQuery(BaseGPTIndexQuery[EmptyIndex]):
    """GPTEmptyIndex query.

    Passes the raw LLM call to the underlying LLM model.

    .. code-block:: python

        response = index.query("<query_str>", mode="default")

    Args:
        input_prompt (Optional[SimpleInputPrompt]): A Simple Input Prompt
            (see :ref:`Prompt-Templates`).

    """

    def __init__(
        self,
        input_prompt: Optional[SimpleInputPrompt] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self._input_prompt = input_prompt or DEFAULT_SIMPLE_INPUT_PROMPT
        super().__init__(**kwargs)

    def retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve relevant nodes."""
        del query_bundle  # Unused
        return []

    def synthesize(
        self,
        query_bundle: QueryBundle,
        nodes: List[NodeWithScore],
        additional_source_nodes: Optional[List[NodeWithScore]] = None,
    ) -> RESPONSE_TYPE:
        """Synthesize answer with relevant nodes."""
        del nodes  # Unused
        del additional_source_nodes  # Unused
        if not self._streaming:
            response, _ = self._service_context.llm_predictor.predict(
                self._input_prompt,
                query_str=query_bundle.query_str,
            )
            return Response(response)
        else:
            llm_predictor = self._service_context.llm_predictor
            response, _ = llm_predictor.predict_with_stream(
                self._input_prompt,
                is_last=True,
                query_str=query_bundle.query_str,
            )
            return Response(response)
    @classmethod
    def from_args(  # type: ignore
        cls,
        response_mode: ResponseMode = ResponseMode.GENERATION,
        **kwargs: Any,
    ) -> BaseGPTIndexQuery:
        if response_mode != ResponseMode.GENERATION:
            raise ValueError("response_mode should not be specified for empty query")

        return super().from_args(
            response_mode=response_mode,
            **kwargs,
        )
