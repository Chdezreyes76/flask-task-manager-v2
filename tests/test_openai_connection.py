#!/usr/bin/env python3
"""
Test exhaustivo para verificar la conexión y configuración de OpenAI vía ai_config.py.

Este test comprueba que la configuración de la API Key y el cliente OpenAI funcionan correctamente.
Incluye chequeos de variables de entorno, estado de configuración y listado de modelos disponibles.
No realiza peticiones de IA, solo verifica la conectividad y configuración.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_openai_connection():
    print("[1] Importando AIConfig...")
    from app.config.ai_config import AIConfig
    print("✅ ai_config.py importado correctamente")
    print("[2] Estado de configuración:")
    status = AIConfig.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")
    print("[3] Comprobando variable de entorno OPENAI_API_KEY...")
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"  Valor leído por os.getenv: {repr(api_key)}")
    print(f"  Valor en AIConfig.OPENAI_API_KEY: {repr(AIConfig.OPENAI_API_KEY)}")
    assert status['configured'], "La API Key de OpenAI no está configurada. Revisa tu archivo .env"
    print("[4] Intentando crear cliente OpenAI...")
    try:
        client = AIConfig.get_client()
        print("✅ Cliente OpenAI creado correctamente")
    except Exception as e:
        print(f"❌ Error al crear cliente OpenAI: {e}")
        assert False, f"Error al crear cliente OpenAI: {e}"
    print("[5] Listando modelos disponibles...")
    try:
        models = client.models.list()
        model_ids = [m.id for m in models.data]
        print(f"  Modelos disponibles ({len(model_ids)}): {model_ids}")
        assert model_ids, "No se encontraron modelos disponibles para esta API key."
    except Exception as e:
        print(f"❌ Error al listar modelos: {e}")
        assert False, f"Error al listar modelos: {e}"
    print("✅ Conexión y configuración de OpenAI comprobadas correctamente.")

if __name__ == "__main__":
    test_openai_connection()
