from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Generic, List, Optional, Union

from mistral_common.exceptions import (
    TokenizerException,
)
from mistral_common.protocol.instruct.messages import (
    UATS,
    AssistantMessageType,
    SystemMessageType,
    ToolMessageType,
    UserMessageType,
)
from mistral_common.protocol.instruct.normalize import InstructRequestNormalizer, normalizer_for_tokenizer_version
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.validator import (
    MistralRequestValidator,
    MistralRequestValidatorV3,
    ValidationMode,
)
from mistral_common.tokens.instruct.request import FIMRequest
from mistral_common.tokens.tokenizers.base import (
    InstructRequest,
    InstructRequestType,
    InstructTokenizer,
    SpecialTokens,
    TokenizedType,
    TokenizerVersion,
)
from mistral_common.tokens.tokenizers.multimodal import (
    ImageEncoder,
    MultimodalConfig,
    MultiModalEncoder,
    SpecialImageIDs,
)
from mistral_common.tokens.tokenizers.sentencepiece import (
    InstructTokenizerV1,
    InstructTokenizerV2,
    InstructTokenizerV3,
    InstructTokenizerV7,
    SentencePieceTokenizer,
    get_mm_config,
    is_sentencepiece,
)
from mistral_common.tokens.tokenizers.tekken import Tekkenizer, is_tekken


def load_mm_encoder(
    mm_config: MultimodalConfig, tokenizer: Union[Tekkenizer, SentencePieceTokenizer]
) -> MultiModalEncoder:
    special_ids = SpecialImageIDs(
        img=tokenizer.get_control_token(SpecialTokens.img.value),
        img_break=tokenizer.get_control_token(SpecialTokens.img_break.value),
        img_end=tokenizer.get_control_token(SpecialTokens.img_end.value),
    )
    return ImageEncoder(mm_config, special_ids)


class MistralTokenizer(
    Generic[UserMessageType, AssistantMessageType, ToolMessageType, SystemMessageType, TokenizedType]
):
    def __init__(
        self,
        instruct_tokenizer: InstructTokenizer[InstructRequest, FIMRequest, TokenizedType, AssistantMessageType],
        validator: MistralRequestValidator[UserMessageType, AssistantMessageType, ToolMessageType, SystemMessageType],
        request_normalizer: InstructRequestNormalizer[
            UserMessageType, AssistantMessageType, ToolMessageType, SystemMessageType, InstructRequestType
        ],
    ):
        self._chat_completion_request_validator = validator
        self._instruct_request_normalizer = request_normalizer
        self.instruct_tokenizer = instruct_tokenizer

    @classmethod
    def _data_path(cls) -> Path:
        return Path(__file__).parents[2] / "data"

    @classmethod
    def v1(cls) -> "MistralTokenizer":
        """open 7B x 8x7B + embed"""
        return cls.from_file(str(cls._data_path() / "tokenizer.model.v1"), mode=ValidationMode.test)

    @classmethod
    def v2(cls) -> "MistralTokenizer":
        """mistral-small // mistral-large"""
        return cls.from_file(
            str(cls._data_path() / "mistral_instruct_tokenizer_240216.model.v2"), mode=ValidationMode.test
        )

    @classmethod
    def v3(cls, is_tekken: bool = False, is_mm: bool = False) -> "MistralTokenizer":
        """open-mixtral-8x22B"""
        if is_tekken and is_mm:
            tokenizer_name = "tekken_240911.json"
        elif is_tekken and not is_mm:
            tokenizer_name = "tekken_240718.json"
        elif not is_tekken and is_mm:
            raise ValueError("Multimodal tokenizer is currently only supported for tekken")
        else:
            tokenizer_name = "mistral_instruct_tokenizer_240323.model.v3"

        return cls.from_file(str(cls._data_path() / tokenizer_name), mode=ValidationMode.test)

    @classmethod
    def v7(cls) -> "MistralTokenizer":
        """mistral-large 2.1"""
        return cls.from_file(
            str(cls._data_path() / "mistral_instruct_tokenizer_241114.model.v7m1"), mode=ValidationMode.test
        )

    @classmethod
    def from_model(cls, model: str) -> "MistralTokenizer":
        model_name_to_tokenizer_cls: Dict[str, Callable[[], MistralTokenizer]] = {
            "open-mistral-7b": MistralTokenizer.v1,
            "open-mixtral-8x7b": MistralTokenizer.v1,
            "mistral-embed": MistralTokenizer.v1,
            "mistral-small-v1": MistralTokenizer.v2,
            "mistral-large-v1": MistralTokenizer.v2,
            "mistral-small": MistralTokenizer.v3,
            "mistral-large": MistralTokenizer.v3,
            "open-mixtral-8x22b": MistralTokenizer.v3,
            "codestral-22b": MistralTokenizer.v3,
            "mistral-nemo": lambda: MistralTokenizer.v3(is_tekken=True),
            "pixtral": lambda: MistralTokenizer.v3(is_tekken=True, is_mm=True),
        }

        # Prefix search the model name mapping
        for model_name, tokenizer_cls in model_name_to_tokenizer_cls.items():
            if model_name in model.lower():
                return tokenizer_cls()

        raise TokenizerException(f"Unrecognized model: {model}")

    @classmethod
    def from_file(
        cls,
        tokenizer_filename: str,
        mode: ValidationMode = ValidationMode.test,
    ) -> "MistralTokenizer":
        """
        Depending on which model we are loading, tokenization and validation might be different. 💩
        """
        tokenizer: Union[SentencePieceTokenizer, Tekkenizer]

        if is_tekken(tokenizer_filename):
            tokenizer = Tekkenizer.from_file(tokenizer_filename)
            mm_config = tokenizer.multimodal
        elif is_sentencepiece(tokenizer_filename):
            tokenizer = SentencePieceTokenizer(tokenizer_filename)
            mm_config = get_mm_config(tokenizer_filename)
        else:
            raise TokenizerException(f"Unrecognized tokenizer file: {tokenizer_filename}")

        mm_encoder = load_mm_encoder(mm_config, tokenizer) if mm_config is not None else None

        request_normalizer = normalizer_for_tokenizer_version(tokenizer.version)

        if tokenizer.version == TokenizerVersion.v1:
            assert mm_encoder is None, "Tokenizer version needs to be >= v3"
            return MistralTokenizer(
                InstructTokenizerV1(tokenizer),
                validator=MistralRequestValidator(mode=mode),
                request_normalizer=request_normalizer,
            )
        elif tokenizer.version == TokenizerVersion.v2:
            assert mm_encoder is None, "Tokenizer version needs to be >= v3"
            return MistralTokenizer(
                InstructTokenizerV2(tokenizer),
                validator=MistralRequestValidator(mode=mode),
                request_normalizer=request_normalizer,
            )
        elif tokenizer.version == TokenizerVersion.v3:
            return MistralTokenizer(
                InstructTokenizerV3(tokenizer, mm_encoder=mm_encoder),
                validator=MistralRequestValidatorV3(mode=mode),
                request_normalizer=request_normalizer,
            )
        elif tokenizer.version == TokenizerVersion.v7:
            return MistralTokenizer(
                InstructTokenizerV7(tokenizer, mm_encoder=mm_encoder),
                validator=MistralRequestValidatorV3(mode=mode),
                request_normalizer=request_normalizer,
            )
        else:
            raise TokenizerException(f"Unrecognized tokenizer filename: {tokenizer_filename}")

        raise TokenizerException(f"Unrecognized tokenizer version: {tokenizer.version}")

    def encode_chat_completion(
        self, request: ChatCompletionRequest[UATS], max_model_input_len: Optional[int] = None
    ) -> TokenizedType:
        validated_request = self._chat_completion_request_validator.validate_request(request)

        if max_model_input_len is None and request.truncate_for_context_length:
            # the max_model_input_len arg should not be optionnal ;
            # but this function is used in many small scripts that have no use
            # for truncation, and don't provide the max model len
            raise TokenizerException(
                "encoding a chat completion request with truncation, but no max model len was provided",
            )

        instruct_request = self._instruct_request_normalizer.from_chat_completion_request(validated_request)

        if request.truncate_for_context_length:
            instruct_request.truncate_at_max_tokens = max_model_input_len

        return self.instruct_tokenizer.encode_instruct(instruct_request)

    def encode_fim(self, request: FIMRequest) -> TokenizedType:
        return self.instruct_tokenizer.encode_fim(request)

    def decode(self, tokens: List[int]) -> str:
        return self.instruct_tokenizer.decode(tokens)
