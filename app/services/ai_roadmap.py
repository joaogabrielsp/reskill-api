import os
import json
import requests
from typing import List, Dict, Any


def gerar_roadmap_ai(usuario) -> List[Dict[str, Any]]:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return _gerar_roadmap_mock(usuario)

    qualidades_list = _parse_qualidades(usuario.qualidades) if hasattr(usuario, 'qualidades') and usuario.qualidades else []

    prompt = f"""
Crie um roadmap de desenvolvimento profissional com EXATAMENTE 7 passos para:

PERFIL DO USUÁRIO:
- Profissão atual: {usuario.profissao}
- Nível de experiência: {usuario.nivel_experience}
- Tempo disponível para estudo: {usuario.tempo_estudo_semanal} horas por semana
- Interesses: {usuario.interesses if hasattr(usuario, 'interesses') else 'Não informado'}
- Qualidades: {', '.join(qualidades_list)}

REGRAS IMPORTANTES:
- Gere EXATAMENTE 7 passos numerados de 1 a 7
- Cada passo deve ser específico para o nível de experiência informado
- Considerar o tempo real de estudo disponível
- Foque em habilidades práticas e demandadas pelo mercado
- Seja específico em recursos reais (plataformas, cursos, ferramentas)
- Inclua apenas o essencial para não sobrecarregar

FORMATO DE RESPOSTA (OBRIGATÓRIO):
Retorne APENAS um JSON válido com esta estrutura exata:
[
  {{
    "id": "1",
    "title": "Título claro e específico do passo",
    "description": "Descrição detalhada do que fazer, com recursos e tempo estimado",
    "order": 1
  }},
  {{
    "id": "2",
    "title": "Título do segundo passo",
    "description": "Descrição com detalhes práticos",
    "order": 2
  }}
  // Continue até o passo 7
]

NÃO inclua textos fora do JSON. Retorne APENAS o JSON.
"""

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um especialista em desenvolvimento de carreira e criação de roadmaps personalizados. Sempre retorne respostas em formato JSON válido sem comentários adicionais."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        roadmap_steps = json.loads(content)

        return _validar_roadmap(roadmap_steps)

    except Exception as e:
        return _gerar_roadmap_mock(usuario)


def _parse_qualidades(qualidades_str: str) -> List[str]:
    try:
        return json.loads(qualidades_str)
    except (json.JSONDecodeError, TypeError):
        return []


def _validar_roadmap(roadmap_steps: List[Dict]) -> List[Dict[str, Any]]:
    if not isinstance(roadmap_steps, list):
        raise ValueError("Resposta deve ser uma lista")

    if len(roadmap_steps) != 7:
        raise ValueError("Roadmap deve ter exatamente 7 passos")

    validated_steps = []
    for i, step in enumerate(roadmap_steps, 1):
        if not isinstance(step, dict):
            continue

        validated_step = {
            "id": str(i),
            "title": step.get("title", f"Passo {i}"),
            "description": step.get("description", "Descrição não disponível"),
            "completed": False,
            "order": i
        }
        validated_steps.append(validated_step)

    return validated_steps


def _gerar_roadmap_mock(usuario) -> List[Dict[str, Any]]:
    return [
        {
            "id": "1",
            "title": "Autoconhecimento e Análise de Mercado",
            "description": "Pesquisar tendências e identificar áreas em crescimento no mercado atual",
            "completed": False,
            "order": 1
        },
        {
            "id": "2",
            "title": "Desenvolver Habilidades Técnicas Fundamentais",
            "description": "Fazer cursos online e praticar as habilidades essenciais para sua área",
            "completed": False,
            "order": 2
        },
        {
            "id": "3",
            "title": "Construir Portfólio de Projetos",
            "description": "Criar projetos práticos que demonstrem suas habilidades para o mercado",
            "completed": False,
            "order": 3
        },
        {
            "id": "4",
            "title": "Networking Estratégico",
            "description": "Conectar-se com profissionais da área e participar de comunidades",
            "completed": False,
            "order": 4
        },
        {
            "id": "5",
            "title": "Certificações e Validações",
            "description": "Obter certificações reconhecidas que validem suas competências",
            "completed": False,
            "order": 5
        },
        {
            "id": "6",
            "title": "Otimizar Perfil Profissional",
            "description": "Atualizar currículo, LinkedIn e outras plataformas profissionais",
            "completed": False,
            "order": 6
        },
        {
            "id": "7",
            "title": "Aplicação para Oportunidades",
            "description": "Candidatar-se a vagas e oportunidades compatíveis com seu novo perfil",
            "completed": False,
            "order": 7
        }
    ]