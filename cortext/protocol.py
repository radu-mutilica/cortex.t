import asyncio
from typing import AsyncIterator, Dict, List, Optional, Union
import bittensor as bt
import pydantic
from starlette.responses import StreamingResponse
import sys


class IsAlive(bt.Synapse):
    answer: Optional[str] = None
    completion: str = pydantic.Field(
        "",
        title="Completion",
        description="Completion status of the current StreamPrompting object. "
                    "This attribute is mutable and can be updated.",
    )


class Bandwidth(bt.Synapse):
    bandwidth_rpm: Optional[Dict[str, dict]] = None


class ImageResponse(bt.Synapse):
    """ A class to represent the response for an image-related request. """
    # https://platform.stability.ai/docs/api-reference#tag/v1generation/operation/textToImage

    completion: Optional[Dict] = pydantic.Field(
        None,
        title="Completion",
        description="The completion data of the image response."
    )

    messages: str = pydantic.Field(
        ...,
        title="Messages",
        description="Messages related to the image response."
    )

    provider: str = pydantic.Field(
        default="OpenAI",
        title="Provider",
        description="The provider to use when calling for your response."
    )

    seed: int = pydantic.Field(
        default=1234,
        title="Seed",
        description="The seed that which to generate the image with"
    )

    samples: int = pydantic.Field(
        default=1,
        title="Samples",
        description="The number of samples to generate"
    )

    cfg_scale: float = pydantic.Field(
        default=8.0,
        title="cfg_scale",
        description="The cfg_scale to use for image generation"
    )

    # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
    sampler: str = pydantic.Field(
        default="",
        title="Sampler",
        description="The sampler to use for image generation"
    )

    steps: int = pydantic.Field(
        default=30,
        title="Seed",
        description="The steps to take in generating the image"
    )

    model: str = pydantic.Field(
        default="dall-e-2",
        title="Model",
        description="The model used for generating the image."
    )

    style: str = pydantic.Field(
        default="vivid",
        title="Style",
        description="The style of the image."
    )

    size: str = pydantic.Field(
        default="1024x1024",
        title="The size of the image, used for Openai generation. Options are 1024x1024, 1792x1024, 1024x1792 for dalle3",
        description="The size of the image."
    )

    height: int = pydantic.Field(
        default=1024,
        title="Height used for non Openai images",
        description="height"
    )

    width: int = pydantic.Field(
        default=1024,
        title="Width used for non Openai images",
        description="width"
    )

    quality: str = pydantic.Field(
        default="standard",
        title="Quality",
        description="The quality of the image."
    )

    uid: int = pydantic.Field(
        default=3,
        title="uid",
        description="The UID to send the synapse to",
    )

    timeout: int = pydantic.Field(
        default=60,
        title="timeout",
        description="The timeout for the dendrite of the synapse",
    )

    required_hash_fields: List[str] = pydantic.Field(
        ["messages"],
        title="Required Hash Fields",
        description="A list of fields required for the hash."
    )

    process_time: int = pydantic.Field(
        default=9999,
        title="process time",
        description="processed time of querying dendrite.",
    )
    task_id: str = pydantic.Field(
        default="9999"
    )

    def deserialize(self) -> Optional[Dict]:
        """ Deserialize the completion data of the image response. """
        return self.completion


class Embeddings(bt.Synapse):
    """ A class to represent the embeddings request and response. """
    provider: str = pydantic.Field(
        default="OpenAI",
        title="text",
        description="Provider name by which embeddings are to be generated"
    )

    texts: List[str] = pydantic.Field(
        ...,
        title="Text",
        description="The list of input texts for which embeddings are to be generated."
    )

    model: str = pydantic.Field(
        default="text-embedding-ada-002",
        title="Model",
        description="The model used for generating embeddings."
    )

    embeddings: Optional[List[List[float]]] = pydantic.Field(
        None,
        title="Embeddings",
        description="The resulting list of embeddings, each corresponding to an input text."
    )

    uid: int = pydantic.Field(
        default=60,
        title="uid",
        description="The UID to send the synapse to",
    )

    timeout: int = pydantic.Field(
        default=60,
        title="timeout",
        description="The timeout for the dendrite of the synapse",
    )


class StreamPrompting(bt.StreamingSynapse):
    messages: List[Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, str]]]]]]] = pydantic.Field(
        ...,
        title="Messages",
        description="A list of messages in the StreamPrompting scenario, "
                    "each containing a role and content. Immutable.",
        allow_mutation=False,
    )

    required_hash_fields: List[str] = pydantic.Field(
        ["messages"],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    seed: int = pydantic.Field(
        default=1234,
        title="Seed",
        description="Seed for text generation. This attribute is immutable and cannot be updated.",
    )

    temperature: float = pydantic.Field(
        default=0.0001,
        title="Temperature",
        description="Temperature for text generation. "
                    "This attribute is immutable and cannot be updated.",
    )

    max_tokens: int = pydantic.Field(
        default=2048,
        title="Max Tokens",
        description="Max tokens for text generation. "
                    "This attribute is immutable and cannot be updated.",
    )

    top_p: float = pydantic.Field(
        default=0.001,
        title="Top_p",
        description="Top_p for text generation. The sampler will pick one of "
                    "the top p percent tokens in the logit distirbution. "
                    "This attribute is immutable and cannot be updated.",
    )

    top_k: int = pydantic.Field(
        default=1,
        title="Top_k",
        description="Top_k for text generation. Sampler will pick one of  "
                    "the k most probablistic tokens in the logit distribtion. "
                    "This attribute is immutable and cannot be updated.",
    )

    completion: Optional[str] = pydantic.Field(
        None,
        title="Completion",
        description="Completion status of the current StreamPrompting object. "
                    "This attribute is mutable and can be updated.",
    )

    provider: str = pydantic.Field(
        default="OpenAI",
        title="Provider",
        description="The provider to use when calling for your response. "
                    "Options: OpenAI, Anthropic, Groq, Bedrock"
    )

    model: str = pydantic.Field(
        default="gpt-3.5-turbo",
        title="model",
        description="""
        The model to use when calling provider for your response.
        For Provider OpenAI:
         text_models = [
            "davinci-002",
            "gpt-4-1106-preview",
            "gpt-4-turbo-preview",
            "gpt-4-0125-preview",
            "babbage-002",
            "gpt-4",
            "gpt-4-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-instruct-0914",
            "gpt-3.5-turbo-instruct",
            "gpt-3.5-turbo-0301",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-4o",
            "gpt-4o-2024-05-13"
        ]
        For Provider Anthropic: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
        For Provider Groq: gemma-7b-it, llama3-70b-8192, llama3-8b-8192, mixtral-8x7b-32768
        For Provider Bedrock: anthropic.claude-3-sonnet-20240229-v1:0, cohere.command-r-v1:0, meta.llama2-70b-chat-v1,
         amazon.titan-text-express-v1, mistral.mistral-7b-instruct-v0:2
        last_updated = 17 June 2024
        """
    )

    uid: int = pydantic.Field(
        default=3,
        title="uid",
        description="The UID to send the streaming synapse to",
    )

    timeout: int = pydantic.Field(
        default=60,
        title="timeout",
        description="The timeout for the dendrite of the streaming synapse",
    )

    streaming: bool = pydantic.Field(
        default=True,
        title="streaming",
        description="whether to stream the output",
    )
    deserialize_flag: bool = pydantic.Field(
        default=True
    )
    task_id: str = pydantic.Field(
        default="9999",
        title="task_id",
        description="task id of the request from this syanpse."
    )
    validator_info: dict = pydantic.Field(
        default={},
        title="validator_info",
    )
    miner_info: dict = pydantic.Field(
        default={},
        title="miner_info",
    )
    time_taken: float = pydantic.Field(
        default=0,
        title="time_taken",
    )
    block_num: int = pydantic.Field(
        default=0,
        title="block_num",
    )
    cycle_num: int = pydantic.Field(
        default=0,
        title="cycle_num",
    )
    epoch_num: int = pydantic.Field(
        default=0,
        title="epoch num",
    )
    score: float = pydantic.Field(
        default=0,
        title="score",
    )
    similarity: float = pydantic.Field(
        default=0,
        title="similarity",
    )

    def to_headers(self) -> dict:
        headers = {"name": self.name, "timeout": str(self.timeout)}

        # Adding headers for 'axon' and 'dendrite' if they are not None
        if self.axon:
            headers.update(
                {
                    f"bt_header_axon_{k}": str(v)
                    for k, v in self.axon.model_dump().items()
                    if v is not None
                }
            )
        if self.dendrite:
            headers.update(
                {
                    f"bt_header_dendrite_{k}": str(v)
                    for k, v in self.dendrite.model_dump().items()
                    if v is not None
                }
            )

        headers[f"bt_header_input_obj_messages"] = "W10="
        headers["header_size"] = str(sys.getsizeof(headers))
        headers["total_size"] = str(self.get_total_size())
        headers["computed_body_hash"] = self.body_hash

        return headers

    async def process_streaming_response(self, response: StreamingResponse, organic=True) -> AsyncIterator[str]:
        if self.completion is None:
            self.completion = ""
        chunk_size = 100 if organic else 1000
        remain_chunk = ""
        try:
            async for chunk in response.content.iter_chunked(chunk_size):
                tokens = chunk.decode("utf-8")
                remain_chunk = tokens
                self.completion += tokens
                yield tokens
        except asyncio.TimeoutError as err:
            # self.completion += remain_chunk
            # yield remain_chunk
            pass

    def extract_response_json(self, response: StreamingResponse) -> dict:
        headers = {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in response.__dict__["_raw_headers"]
        }

        def extract_info(prefix: str) -> dict[str, str]:
            return {
                key.split("_")[-1]: value
                for key, value in headers.items()
                if key.startswith(prefix)
            }

        return {
            "name": headers.get("name", ""),
            "timeout": float(headers.get("timeout", 0)),
            "total_size": int(headers.get("total_size", 0)),
            "header_size": int(headers.get("header_size", 0)),
            "dendrite": extract_info("bt_header_dendrite"),
            "axon": extract_info("bt_header_axon"),
            "messages": self.messages,
            "completion": self.completion,
            "provider": self.provider,
            "model": self.model,
            "seed": self.seed,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "timeout": self.timeout,
            "streaming": self.streaming,
            "uid": self.uid,
        }
