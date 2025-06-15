import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#!/usr/bin/env python3
"""
Test de integración real para OpenAIService usando tareas existentes del sistema.

Este test ejecuta los métodos principales de OpenAIService sobre las tareas reales almacenadas en 'app/data/tasks.json'.
Verifica que la generación de descripciones, categorización y estimación de esfuerzo funcionan correctamente y muestra los tokens usados.
No modifica datos, solo lee y muestra resultados por consola.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_openai_service_with_real_tasks():
    from app.services.ai_service import OpenAIService
    service = OpenAIService()
    print("✅ Servicio OpenAIService instanciado correctamente")

    # Cargar tareas reales
    with open('app/data/tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    print(f"\n📄 {len(tasks)} tareas cargadas de tasks.json\n")

    for i, task in enumerate(tasks, 1):
        print(f"--- Tarea {i}: {task['title']} ---")
        # 1. Generar descripción
        print("\n🔎 generate_description:")
        result = service.generate_description(task)
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Descripción generada: {result['result']}")
            print(f"Tokens usados: {result['total_tokens']}")

        # 2. Clasificar tarea
        print("\n🔎 categorize_task:")
        result2 = service.categorize_task(task)
        if "error" in result2:
            print(f"❌ Error: {result2['error']}")
        else:
            print(f"✅ Categoría sugerida: {result2['result']}")

        # 3. Estimar esfuerzo
        print("\n🔎 estimate_effort:")
        result3 = service.estimate_effort(task)
        if "error" in result3:
            print(f"❌ Error: {result3['error']}")
        else:
            print(f"✅ Esfuerzo estimado: {result3['result']}")
            print(f"Tokens usados: {result3['total_tokens']}")

if __name__ == "__main__":
    test_openai_service_with_real_tasks()
