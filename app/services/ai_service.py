"""
Servicio centralizado para interacción con OpenAI y gestión de prompts y tokens.
"""
import time
from typing import Any, Dict, Optional
from openai import OpenAI, OpenAIError
import tiktoken
from app.config.ai_config import AIConfig

class OpenAIService:
    """
    Servicio para gestionar peticiones a OpenAI, prompts y conteo de tokens.
    """
    def __init__(self):
        self.client = AIConfig.get_client()
        self.model = AIConfig.DEFAULT_MODEL
        self.tokenizer = tiktoken.encoding_for_model(self.model)

    def _count_tokens(self, text: str) -> int:
        """Cuenta el número de tokens en un texto usando tiktoken."""
        return len(self.tokenizer.encode(text))

    def _build_prompt(self, system_prompt: str, user_prompt: str) -> list:
        """Construye el prompt para el modelo OpenAI (formato chat)."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def _call_openai(self, messages: list, operation: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Llama a la API de OpenAI y maneja errores comunes.
        Returns: dict con respuesta, tokens y tiempos.
        """
        if params is None:
            params = AIConfig.get_model_params(operation)
        else:
            default = AIConfig.get_model_params(operation)
            default.update(params)
            params = default
        start = time.time()
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                **params
            )
            end = time.time()
            usage = response.usage if hasattr(response, 'usage') else None
            return {
                "result": response.choices[0].message.content.strip(),
                "input_tokens": usage.prompt_tokens if usage else None,
                "output_tokens": usage.completion_tokens if usage else None,
                "total_tokens": usage.total_tokens if usage else None,
                "processing_time": round(end - start, 3),
                "model": params["model"]
            }
        except OpenAIError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Error inesperado: {e}"}

    def generate_description(self, task_data: dict) -> dict:
        """
        Genera una descripción para una tarea usando IA.
        """
        system_prompt = AIConfig.get_system_prompt('describe')
        user_prompt = f"Título: {task_data.get('title')}\nPrioridad: {task_data.get('priority')}\nPersona asignada: {task_data.get('assigned_to')}\nCategoría: {task_data.get('category', 'No especificada')}"
        messages = self._build_prompt(system_prompt, user_prompt)
        return self._call_openai(messages, operation='describe')

    def categorize_task(self, task_data: dict) -> dict:
        """
        Clasifica una tarea por categoría usando IA.
        """
        system_prompt = AIConfig.get_system_prompt('categorize')
        user_prompt = f"Título: {task_data.get('title')}\nDescripción: {task_data.get('description')}"
        messages = self._build_prompt(system_prompt, user_prompt)
        return self._call_openai(messages, operation='categorize')

    def estimate_effort(self, task_data: dict) -> dict:
        """
        Estima el esfuerzo en horas para una tarea usando IA.
        """
        system_prompt = AIConfig.get_system_prompt('estimate')
        user_prompt = f"Título: {task_data.get('title')}\nDescripción: {task_data.get('description')}\nCategoría: {task_data.get('category', 'No especificada')}"
        messages = self._build_prompt(system_prompt, user_prompt)
        return self._call_openai(messages, operation='estimate')

    def analyze_risks(self, task_data: dict) -> dict:
        """
        Genera solo el análisis de riesgos usando IA.
        """
        system_prompt = AIConfig.get_system_prompt('audit')
        user_prompt = (
            f"Título: {task_data.get('title')}\n"
            f"Descripción: {task_data.get('description')}\n"
            f"Categoría: {task_data.get('category', 'No especificada')}"
        )
        messages = self._build_prompt(system_prompt, user_prompt)
        return self._call_openai(messages, operation='audit')

    def generate_mitigation(self, task_data: dict, risk_analysis: str) -> dict:
        """
        Genera solo el plan de mitigación de riesgos usando IA, tomando en cuenta el análisis de riesgos previo.
        """
        system_prompt = AIConfig.get_system_prompt('mitigation_plan')
        user_prompt = (
            f"Título: {task_data.get('title')}\n"
            f"Descripción: {task_data.get('description')}\n"
            f"Categoría: {task_data.get('category', 'No especificada')}\n"
            f"Análisis de riesgos: {risk_analysis}"
        )
        messages = self._build_prompt(system_prompt, user_prompt)
        return self._call_openai(messages, operation='mitigation_plan')
