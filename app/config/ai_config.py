"""
Configuración para servicios de IA (OpenAI)
"""
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=ENV_PATH, override=True)

class AIConfig:
    """Configuración centralizada para servicios de IA"""
    
    # API Key de OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Modelos disponibles
    DEFAULT_MODEL = "gpt-4o-mini"
    MODELS = {
        'fast': 'gpt-3.5-turbo',
        'balanced': 'gpt-4o-mini',
        'quality': 'gpt-4o'
    }
    
    # Parámetros por defecto para diferentes operaciones
    DEFAULT_PARAMS = {
        'temperature': 0.7,
        'max_tokens': 1000,
        'top_p': 1.0,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }
    
    # Parámetros específicos por tipo de operación
    OPERATION_PARAMS = {
        'describe': {
            'temperature': 0.8,
            'max_tokens': 500
        },
        'categorize': {
            'temperature': 0.3,
            'max_tokens': 50
        },
        'estimate': {
            'temperature': 0.2,
            'max_tokens': 100
        },
        'audit': {
            'temperature': 0.6,
            'max_tokens': 800
        }
    }
    
    # Prompts del sistema para cada operación
    SYSTEM_PROMPTS = {
        'describe': """Eres un experto en gestión de proyectos de software. \
        Tu tarea es generar descripciones claras y detalladas para tareas de desarrollo.\
        La descripción debe ser específica, técnica y orientada a la acción.\
        Responde solo con la descripción, sin explicaciones adicionales.""",
        
        'categorize': """Eres un clasificador de tareas de desarrollo de software.\
        Debes clasificar cada tarea en una de estas categorías exactas:\
        - Frontend\
        - Backend  \
        - Testing\
        - DevOps\
        - Database\
        - Documentation\
        - Security\
        - Performance\
        - Bug Fix\
        - Feature\
        Responde solo con el nombre de la categoría, nada más.""",
        
        'estimate': """Eres un experto en estimación de esfuerzo para desarrollo de software.\
        Debes estimar las horas necesarias para completar una tarea considerando:\
        - Complejidad técnica\
        - Dependencias\
        - Testing requerido\
        - Documentación\
        Responde solo con un número entero de horas.""",
        
        'audit': """Eres un especialista en análisis de riesgos para proyectos de software.\
        Tu tarea es identificar riesgos potenciales en la tarea proporcionada.\
        Devuelve solo el ANÁLISIS DE RIESGOS, sin incluir ningún plan de mitigación ni explicaciones adicionales.""",

        'mitigation_plan': """Eres un especialista en mitigación de riesgos para proyectos de software.\
        Se te proporcionará un análisis de riesgos.\
        Tu tarea es proponer un PLAN DE MITIGACIÓN detallado y específico para cada riesgo identificado.\
        Devuelve solo el plan de mitigación, sin repetir el análisis de riesgos ni añadir explicaciones adicionales."""
    }
    
    # Configuración de costos (USD por 1K tokens)
    TOKEN_COSTS = {
        'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
        'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
        'gpt-4o': {'input': 0.03, 'output': 0.06}
    }
    
    @classmethod
    def get_client(cls) -> OpenAI:
        """
        Obtiene el cliente configurado de OpenAI
        
        Returns:
            OpenAI: Cliente configurado
            
        Raises:
            ValueError: Si no se encuentra la API key
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY no encontrada. "
                "Por favor configura tu API key en el archivo .env"
            )
        
        return OpenAI(api_key=cls.OPENAI_API_KEY)
    
    @classmethod
    def get_model_params(cls, operation: str, model: str = None) -> Dict[str, Any]:
        """
        Obtiene los parámetros configurados para una operación específica
        
        Args:
            operation: Tipo de operación (describe, categorize, estimate, audit)
            model: Modelo a usar (opcional, usa DEFAULT_MODEL si no se especifica)
            
        Returns:
            Dict con los parámetros configurados
        """
        params = cls.DEFAULT_PARAMS.copy()
        
        # Aplicar parámetros específicos de la operación
        if operation in cls.OPERATION_PARAMS:
            params.update(cls.OPERATION_PARAMS[operation])
        
        # Configurar modelo
        params['model'] = model or cls.DEFAULT_MODEL
        
        return params
    
    @classmethod
    def get_system_prompt(cls, operation: str) -> str:
        """
        Obtiene el prompt del sistema para una operación específica
        
        Args:
            operation: Tipo de operación
            
        Returns:
            String con el prompt del sistema
        """
        return cls.SYSTEM_PROMPTS.get(operation, "")
    
    @classmethod
    def get_token_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calcula el costo estimado de una operación
        
        Args:
            model: Modelo utilizado
            input_tokens: Tokens de entrada
            output_tokens: Tokens de salida
            
        Returns:
            Costo estimado en USD
        """
        if model not in cls.TOKEN_COSTS:
            return 0.0
        
        costs = cls.TOKEN_COSTS[model]
        input_cost = (input_tokens / 1000) * costs['input']
        output_cost = (output_tokens / 1000) * costs['output']
        
        return input_cost + output_cost
    
    @classmethod
    def is_configured(cls) -> bool:
        """
        Verifica si la configuración de AI está completa
        
        Returns:
            True si está configurado correctamente
        """
        return bool(cls.OPENAI_API_KEY)
    
    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """
        Obtiene el estado de la configuración
        
        Returns:
            Dict con información del estado
        """
        return {
            'configured': cls.is_configured(),
            'api_key_present': bool(cls.OPENAI_API_KEY),
            'default_model': cls.DEFAULT_MODEL,
            'available_models': list(cls.MODELS.values()),
            'operations_supported': list(cls.SYSTEM_PROMPTS.keys())
        }