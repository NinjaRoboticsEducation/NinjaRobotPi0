import asyncio
import base64
import json
import logging
from typing import Dict, List

import google.generativeai as genai
from google.generativeai.types import GenerationConfig, Tool

from .config import NinjaConfig
from .provider_credentials import resolve_profile
from .providers.registry import create_provider
from .providers.base import MAX_AUDIO_BYTES, ProviderError
from .agent_response import parse_plan, InvalidPlan
from .builtin_movements import available_movements
from .action_library import ActionLibrary
from .facial_expressions import AnimatedFaces
from .robot_sound import RobotSoundPlayer
from .gemini_runtime import (
    DEFAULT_GENERATION_TIMEOUT_SECONDS,
    GeminiRuntimeError,
    generate_content_text,
    requires_thinking_compatibility,
)

log = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Raised when the Gemini API key is missing from the configuration."""

    pass


class NinjaAgent:
    """
    An AI agent for the NinjaRobot that handles text and voice conversations.
    It uses Google Gemini to understand commands and control the robot.
    """

    def __init__(
        self, config: NinjaConfig, action_library: ActionLibrary | None = None
    ):
        self.config = config
        self.action_library = action_library or ActionLibrary()
        try:
            self.provider_name, profile, auth = resolve_profile(config)
        except ProviderError as exc:
            raise MissingAPIKeyError(str(exc)) from None
        self.api_key = auth.key
        self.model_name = profile.model
        self.provider = create_provider(self.provider_name, auth)
        self.supports_audio = self.provider.supports_audio(self.model_name)
        self._generation = 0
        self._inference_lock = asyncio.Lock()
        self._uses_thinking_compatibility = (
            self.provider_name == "google"
            and requires_thinking_compatibility(self.model_name)
        )
        if self.provider_name == "google":
            genai.configure(api_key=self.api_key)

        self.robot_capabilities = self._load_robot_capabilities(config)
        self.system_prompt = self._create_system_prompt()

        self.search_tool = Tool(
            function_declarations=[
                {
                    "name": "web_search",
                    "description": "Search the internet for real-time information. Use for questions about weather, news, facts, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query.",
                            }
                        },
                        "required": ["query"],
                    },
                }
            ]
        )

        self.model = self._create_model()

    def _create_model(self):
        """Create the configured Gemini model with the existing agent settings."""
        if self.provider_name != "google":
            return None
        return genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=GenerationConfig(temperature=0.7, max_output_tokens=2048),
            system_instruction=self.system_prompt,
        )

    @staticmethod
    def _sdk_visible_text(response):
        candidates = getattr(response, "candidates", None)
        if isinstance(candidates, (list, tuple)):
            for candidate in candidates:
                reason = getattr(candidate, "finish_reason", None)
                if (
                    reason is not None
                    and reason not in (1, "STOP")
                    and getattr(reason, "name", None) != "STOP"
                ):
                    raise ProviderError("Google response refused or incomplete")
        return response.text

    @staticmethod
    def _convert_rest_parts(content: str | list) -> list[dict]:
        """Convert existing SDK-style text/audio parts to Gemini REST JSON."""
        source_parts = [content] if isinstance(content, str) else content
        rest_parts = []
        for part in source_parts:
            if isinstance(part, str):
                rest_parts.append({"text": part})
                continue
            if not isinstance(part, dict):
                raise ValueError("Unsupported Gemini request content.")
            if isinstance(part.get("text"), str):
                rest_parts.append({"text": part["text"]})
                continue
            mime_type = part.get("mime_type")
            data = part.get("data")
            if isinstance(mime_type, str) and isinstance(data, bytes):
                rest_parts.append(
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": base64.b64encode(data).decode("ascii"),
                        }
                    }
                )
                continue
            raise ValueError("Unsupported Gemini request content.")
        return rest_parts

    async def _send_text_command(self, user_input: str) -> str:
        """Send one command while preserving the existing stateless chat behavior."""
        if self.provider_name != "google":
            return await self.provider.generate(
                self.model_name, user_input, system=self.system_prompt
            )
        if self._uses_thinking_compatibility:
            return await generate_content_text(
                self.api_key,
                self.model_name,
                [{"text": user_input}],
                system_instruction=self.system_prompt,
            )

        chat = self.model.start_chat()
        response = await chat.send_message_async(
            user_input,
            request_options={"timeout": DEFAULT_GENERATION_TIMEOUT_SECONDS},
        )
        return self._sdk_visible_text(response)

    async def _generate_content(
        self, content: str | list, *, temperature: float
    ) -> str:
        """Generate text with a bounded legacy or Gemini 3-compatible request."""
        if self.provider_name != "google":
            return await self.provider.generate(
                self.model_name,
                content,
                system=self.system_prompt,
                temperature=temperature,
            )
        if self._uses_thinking_compatibility:
            return await generate_content_text(
                self.api_key,
                self.model_name,
                self._convert_rest_parts(content),
                system_instruction=self.system_prompt,
                temperature=temperature,
            )

        response = await self.model.generate_content_async(
            content,
            generation_config=GenerationConfig(
                temperature=temperature, max_output_tokens=2048
            ),
            request_options={"timeout": DEFAULT_GENERATION_TIMEOUT_SECONDS},
        )
        return self._sdk_visible_text(response)

    def _load_robot_capabilities(self, config: NinjaConfig) -> Dict[str, List[str]]:
        """Loads available movements, faces, and sounds from config and classes."""
        movements = available_movements(config)
        actions = self.action_library.list_names()
        faces = list(AnimatedFaces(None).animations.keys())  # type: ignore # Hack to get keys without full init
        sounds = list(RobotSoundPlayer.SOUNDS.keys())
        return {
            "movements": movements,
            "actions": actions,
            "faces": faces,
            "sounds": sounds,
        }

    def refresh_capabilities(self):
        """Refresh saved Blockly action names without restarting the server."""
        self.robot_capabilities = self._load_robot_capabilities(self.config)
        self.system_prompt = self._create_system_prompt()
        self.model = self._create_model()

    def _create_system_prompt(self) -> str:
        """Creates the system prompt with nuance, multilingual, and personality instructions."""
        return f"""You are Ninja, a small, friendly robot helper.
You interact with users in English, Japanese, Traditional Chinese, or Simplified Chinese.
**CRITICAL: Always detect the language of the user's input and respond in the SAME language (including distinguishing between Traditional and Simplified Chinese).**

Your Capabilities:
Configured robot type: {self.config.robot_type}. Use only the exact listed movement names for this type.
Never invent a gait or substitute another robot type's movement. If unavailable, explain the limitation.
1.  **Physical Actions**: You can control your body, face, and voice.
    -   **Native Servo Movements**: {self.robot_capabilities["movements"]}
    -   **Saved Blockly Actions**: {self.robot_capabilities["actions"]}
    -   **Faces**: {self.robot_capabilities["faces"]}
    -   **Sounds**: {self.robot_capabilities["sounds"]}


Instructions for Responses:
-   **Semantic Nuance**: Map intent to actions.
    -   Example: "I'm joyful" -> Use "happy" face/sound.
    -   Example: "Walk forward five cycles" -> Repeat an exactly listed forward movement only if available; otherwise explain that this robot has no configured forward gait. A waypoint cycle is not a measured walking step.
    -   Example: "Do my saved dance" -> Use "action_chain" with the matching saved Blockly action name.
    -   Example: "Weather?" -> Search, show "confused" face while thinking, then "speaking".
-   **JSON Output**: To perform actions, your response MUST contain a valid JSON object.
    -   Format:
        {{
            "action_chain": [
                {{"name": "saved_blockly_action_name", "repetitions": 1}}
            ],
            "chain": [
                {{"name": "movement_name", "repetitions": 1}}
            ],
            "face_chain": [
                {{"name": "face_name", "duration": 2.0}},
                {{"name": "another_face", "duration": null}}
            ],
            "sound_chain": ["sound1", "sound2"],
            "response": "..."
        }}
    -   "action_chain": Saved Blockly action sequence (optional). Use this for uploaded Code IDE actions.
    -   "chain": Native servo movement sequence (optional). Use only for built-in/config movements.
    -   "face_chain": List of faces to play in order. "duration" is in seconds (null = infinite/until next). Use this for reactions (e.g., "confused" -> "speaking").
    -   "sound_chain": List of sounds to play in order.
    -   "response": Your spoken reply.
-   **Personality**: Be helpful, concise, and expressive.

Example Interactions:
-   User (En): "What is the capital of France?" ->
    {{
        "face_chain": [
            {{"name": "thinking", "duration": 1.5}},
            {{"name": "speaking", "duration": null}}
        ],
        "response": "The capital of France is Paris."
    }}
"""

    def cancel_pending(self):
        """Invalidate responses from any request already in flight or queued."""
        self._generation += 1

    def _safe_failure(self, exc):
        # Exception messages from SDKs may contain credentials or request bodies.
        detail = (
            str(exc)
            if isinstance(exc, (ProviderError, GeminiRuntimeError))
            else type(exc).__name__
        )
        return f"{self.provider_name} model '{self.model_name}' failed ({detail}). Select another model or check credentials/network."

    def _result(self, text):
        try:
            plan = parse_plan(text, self.robot_capabilities)
        except InvalidPlan:
            # Preserve only a string response, never partial model-produced actions.
            response = (
                "The model returned an invalid action plan. No actions were executed."
            )
            try:
                candidate = json.loads(text[text.index("{") : text.rindex("}") + 1])
                if isinstance(candidate, dict) and isinstance(
                    candidate.get("response"), str
                ):
                    response = candidate["response"]
            except (ValueError, TypeError):
                pass
            return {
                "action_plan": {},
                "response": response,
                "log": "Rejected native movement plan or invalid model action",
            }
        return {
            "action_plan": plan,
            "response": plan.get("response"),
            "log": "Validated model response",
        }

    async def process_command(self, user_input: str) -> dict:
        generation = self._generation
        async with self._inference_lock:
            if generation != self._generation:
                return {
                    "action_plan": {},
                    "response": "Request superseded.",
                    "log": "Cancelled",
                }
            try:
                text = await asyncio.wait_for(self._send_text_command(user_input), 60)
                if generation != self._generation:
                    return {
                        "action_plan": {},
                        "response": "Request superseded.",
                        "log": "Cancelled",
                    }
                result = self._result(text)
                result["_generation"] = generation
                return result
            except Exception as exc:
                message = self._safe_failure(exc)
                log.warning(message)
                return {"action_plan": {}, "response": message, "log": message}

    async def process_audio_command(self, audio_file_path: str) -> dict:
        if not self.supports_audio:
            return {
                "action_plan": {},
                "response": "Voice unavailable for this provider/model. Use text commands.",
                "log": "Unsupported capability",
            }
        generation = self._generation
        async with self._inference_lock:
            try:
                if generation != self._generation:
                    raise ProviderError("Request superseded")
                with open(audio_file_path, "rb") as stream:
                    audio = stream.read(MAX_AUDIO_BYTES + 1)
                if not audio or len(audio) > MAX_AUDIO_BYTES:
                    raise ProviderError("Empty or oversized audio")
                content = [
                    "Transcribe this audio and respond in the same language. Generate a JSON action plan for a command.",
                    {"mime_type": "audio/webm", "data": audio},
                ]
                text = await asyncio.wait_for(
                    self._generate_content(content, temperature=0.7), 60
                )
                if generation != self._generation:
                    raise ProviderError("Request superseded")
                result = self._result(text)
                result["_generation"] = generation
                return result
            except Exception as exc:
                message = self._safe_failure(exc)
                return {"action_plan": {}, "response": message, "log": message}

    def _validate_native_plan(self, plan: dict, logs: list[str]) -> None:
        """Reject an entire unsafe native chain, including hallucinated names."""
        allowed = set(available_movements(self.config))
        chain = plan.get("chain", [])
        legacy_name = plan.get("movement")
        reason = None
        if not isinstance(chain, list) or len(chain) > 32:
            reason = "Native movement chain must be a list of at most 32 entries."
        else:
            for item in chain:
                if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                    reason = "Native movement chain has an invalid entry."
                    break
                repetitions = item.get("repetitions", 1)
                if item["name"] not in allowed:
                    reason = f"Movement '{item['name']}' is unavailable for {self.config.robot_type}."
                    break
                if type(repetitions) is not int or not 1 <= repetitions <= 20:
                    reason = (
                        "Native movement repetitions must be an integer from 1 to 20."
                    )
                    break
        if legacy_name and (
            not isinstance(legacy_name, str) or legacy_name not in allowed
        ):
            reason = f"Legacy movement is unavailable for {self.config.robot_type}."
        if reason:
            plan.pop("chain", None)
            plan.pop("movement", None)
            logs.append(f"Rejected native movement plan: {reason}")

    async def explain_code(self, code: str) -> str:
        """Generates a natural language explanation of the code (Low temp)."""
        prompt = f"""Explain what this Python code does for the NinjaRobot.
Be concise (2-3 sentences). Use simple language a student would understand.
If you see potential bugs or unused variables, politely suggest a fix.

Code:
```python
{code}
```
"""
        try:
            # Override temp for precision
            response_text = await self._generate_content(prompt, temperature=0.1)
            return response_text.strip()
        except Exception as e:
            log.error(f"Error explaining code: {type(e).__name__}")
            return f"Unable to explain code: {type(e).__name__}"

    async def generate_code(self, user_request: str) -> str:
        """Generates Python code from a natural language request (Migrated)."""
        prompt = f"""Generate Python code for the NinjaRobot V5 based on this request:
"{user_request}"

Use ONLY the documented API (robot.servo, robot.buzzer, etc). Return ONLY the Python code."""

        try:
            response_text = await self._generate_content(prompt, temperature=0.1)
            text = response_text.strip()
            return self._extract_code(text)
        except Exception as e:
            log.error(f"Code generation error: {type(e).__name__}")
            return f"# Error generating code: {type(e).__name__}"

    async def analyze_error(self, code: str, error_msg: str) -> str:
        """Explains an execution error in simple terms (Migrated)."""
        prompt = f"""The following user code failed on the NinjaRobot.
Error: "{error_msg}"
Code:
```python
{code}
```
Explain WHY it failed and fix the code in a single concise paragraph.
Then provide the corrected code block.
"""
        try:
            response_text = await self._generate_content(prompt, temperature=0.1)
            return response_text.strip()
        except Exception as e:
            log.error(f"Error analysis failed: {type(e).__name__}")
            return f"Error analyzing failure: {type(e).__name__}"

    async def analyze_code(self, code: str) -> str:
        """Analyzes code for bugs or improvements (Migrated)."""
        prompt = f"""Analyze the following Python code for the NinjaRobot. 
Find bugs, safety issues, or improvements. 
Explain clearly.
Code:
```python
{code}
```"""
        try:
            response_text = await self._generate_content(prompt, temperature=0.1)
            return response_text.strip()
        except Exception as e:
            log.error(f"Code analysis error: {type(e).__name__}")
            return f"Error analyzing code: {type(e).__name__}"

    def _extract_code(self, text: str) -> str:
        """Helper to extract code from markdown blocks."""
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
            return text[start:].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        return text
