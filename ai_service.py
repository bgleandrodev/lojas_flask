import os
import logging
import re
import random
from typing import List, Dict, Optional
from collections import deque
import requests

logger = logging.getLogger(__name__)

# ============================================================================
# BASE DE CONHECIMENTO DOS PRODUTOS
# ============================================================================

PRODUCT_DETAILS = {
    "Teclado Mecânico": {
        "categoria": "Acessórios",
        "preco": 250.00,
        "descricao_longa": "Teclado mecânico com switches azuis (clicky), ideal para digitação e jogos. RGB, construção em metal, 50M toques.",
        "popularidade": 5
    },
    "Mouse Gamer": {
        "categoria": "Acessórios",
        "preco": 150.00,
        "descricao_longa": "Mouse óptico com DPI ajustável até 6400, 6 botões, RGB, ergonômico.",
        "popularidade": 4
    },
    'Monitor 24"': {
        "categoria": "Periféricos",
        "preco": 1200.00,
        "descricao_longa": "Monitor LED 24\" Full HD, IPS, 75Hz, HDMI/DisplayPort.",
        "popularidade": 4
    },
    "Headset Bluetooth": {
        "categoria": "Áudio",
        "preco": 300.00,
        "descricao_longa": "Headset sem fio Bluetooth 5.0, ANC, bateria 30h.",
        "popularidade": 4
    },
    "Notebook Gamer": {
        "categoria": "Computadores",
        "preco": 5000.00,
        "descricao_longa": "Notebook gamer i7, RTX 3060, 16GB RAM, SSD 512GB.",
        "popularidade": 5
    },
    "SSD 1TB": {
        "categoria": "Armazenamento",
        "preco": 600.00,
        "descricao_longa": "SSD 1TB SATA III, leitura 560MB/s, ideal para upgrade.",
        "popularidade": 4
    },
    "Kit de Organização de Cabos": {
        "categoria": "Eletrônicos",
        "preco": 50.00,
        "descricao_longa": "Kit com presilhas e braçadeiras para organizar cabos.",
        "popularidade": 3
    }
}

KEYWORD_TO_PRODUCT = {
    "teclado": "Teclado Mecânico",
    "mouse": "Mouse Gamer",
    "monitor": "Monitor 24\"",
    "headset": "Headset Bluetooth",
    "notebook": "Notebook Gamer",
    "ssd": "SSD 1TB"
}


class ConversationalMemory:
    def __init__(self, max_history: int = 10):
        self.history = deque(maxlen=max_history)
        self.last_recommended = None
        self.last_recommended_price = None
        self.budget_mentioned = None

    def add_interaction(self, user_query: str, ai_response: str):
        self.history.append({"user": user_query, "ai": ai_response[:500]})
        budget = self._extract_budget(user_query)
        if budget:
            self.budget_mentioned = budget
        # Extrai produto da resposta
        match = re.search(r'\*\*([^*]+)\*\*', ai_response)
        if match:
            self.last_recommended = match.group(1)
            price_match = re.search(r'R\$\s*(\d+(?:\.\d+)?)', ai_response)
            if price_match:
                self.last_recommended_price = float(price_match.group(1))

    def _extract_budget(self, text: str) -> Optional[float]:
        patterns = [
            r'at[eé]\s*R?\$?\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*reais? (?:é o meu limite|de limite|é o máximo)',
            r'orçamento de\s*R?\$?\s*(\d+(?:\.\d+)?)',
            r'limite de\s*R?\$?\s*(\d+(?:\.\d+)?)',
            r'at[eé]\s*(\d+(?:\.\d+)?)\s*reais?',
        ]
        for pat in patterns:
            match = re.search(pat, text.lower())
            if match:
                val = float(match.group(1))
                if 10 <= val <= 100000:
                    return val
        return None

    def get_context(self) -> str:
        parts = []
        if self.budget_mentioned:
            parts.append(f"Orçamento do cliente: R$ {self.budget_mentioned:.2f}")
        if self.last_recommended and self.last_recommended_price:
            parts.append(f"Último produto recomendado: {self.last_recommended} (R$ {self.last_recommended_price:.2f})")
        elif self.last_recommended:
            parts.append(f"Último produto recomendado: {self.last_recommended}")
        return "\n".join(parts) if parts else "Nenhum contexto anterior."


def force_portuguese(text: str) -> str:
    if not isinstance(text, str):
        return text
    subs = {
        r'\bsomething\b': 'algo', r'\bgood\b': 'bom', r'\bbest\b': 'melhor',
        r'\bgreat\b': 'ótimo', r'\bexcellent\b': 'excelente',
        r'\bprice\b': 'preço', r'\bbudget\b': 'orçamento', r'\bproducts\b': 'produtos',
        r'\brecommend\b': 'recomendo', r'\boption\b': 'opção'
    }
    for pat, rep in subs.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("AI_MODEL", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free")
        self.temperature = 0.85
        self.max_tokens = 900
        self.enabled = os.getenv("AI_ENABLED", "true").lower() == "true"
        self.timeout = 35
        self.memory = ConversationalMemory()
        logger.info("✅ IA Service inicializado")

    def is_available(self) -> bool:
        return self.enabled and bool(self.api_key) and len(self.api_key) > 20

    def get_completion(self, prompt: str) -> Optional[str]:
        if not self.is_available():
            return None
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                return force_portuguese(content) if content else None
            else:
                logger.error(f"Erro API: {resp.status_code}")
                return None
        except Exception as e:
            logger.error(f"Erro: {e}")
            return None

    def recommend_products(self, user_query: str, products: List[Dict]) -> str:
        # prepara o contexto
        context = self.memory.get_context()

        # ordena os produtos por preço
        sorted_by_price = sorted(products, key=lambda x: x['preco'])
        product_lines = "\n".join([
            f"- {p['nome']}: R$ {p['preco']:.2f} ({p['categoria']})"
            for p in sorted_by_price
        ])

        budget = self.memory.budget_mentioned
        budget_str = f"ORÇAMENTO DO CLIENTE: ATÉ R$ {budget:.2f}" if budget else "O cliente NÃO definiu um orçamento específico."

        prompt = f"""Você é um vendedor de tecnologia brasileiro, simpático e flexível.

CONTEXTO DA CONVERSA:
{context}

CATÁLOGO DE PRODUTOS (ordenado por preço do mais barato ao mais caro):
{product_lines}

{budget_str}

PERGUNTA ATUAL DO CLIENTE:
"{user_query}"

INSTRUÇÕES IMPORTANTES:
1. Responda APENAS em português brasileiro, de forma natural e útil.
2. **Se o cliente pedir "algo mais caro" ou "produto melhor"**:
   - Compare com o ÚLTIMO PRODUTO RECOMENDADO (se houver).
   - Procure no catálogo um produto com PREÇO MAIOR que o último, que ainda respeite o orçamento.
   - **Se NÃO existir** nenhum produto mais caro dentro do orçamento, informe claramente: "Não há produtos mais caros que [produto] dentro do seu orçamento de R$ [valor]."
3. **Se o cliente pedir "algo mais barato"**:
   - Procure um produto com PREÇO MENOR que o último recomendado.
4. Recomende UM produto do catálogo. Destaque o nome entre ** ** e o preço.
5. Termine perguntando se o cliente quer mais detalhes.

RESPOSTA:"""

        result = self.get_completion(prompt)
        if result:
            self.memory.add_interaction(user_query, result)
            match = re.search(r'\*\*([^*]+)\*\*', result)
            if match:
                self.memory.last_recommended = match.group(1)
                price_match = re.search(r'R\$\s*(\d+(?:\.\d+)?)', result)
                if price_match:
                    self.memory.last_recommended_price = float(price_match.group(1))
            return result

        # ================================================================
        # FALLBACK INTELIGENTE (caso / quando a IA não responde)
        # ================================================================
        logger.warning("⚠️ IA não respondeu. Usando fallback.")

        budget = self.memory.budget_mentioned
        last_prod_name = self.memory.last_recommended
        last_prod_price = self.memory.last_recommended_price

        # log para debug
        logger.info(f"Fallback - Orçamento: {budget}, Último produto: {last_prod_name} (R$ {last_prod_price})")

        # filtra pelo orçamento do cliente
        if budget:
            candidates = [p for p in products if p['preco'] <= budget]
        else:
            candidates = products

        if not candidates:
            candidates = products

        # detecta intenção básica
        query_lower = user_query.lower()
        asking_for_cheaper = any(p in query_lower for p in ["mais barato", "mais em conta", "menor preço"])
        asking_for_dearer = any(p in query_lower for p in ["mais caro", "melhor", "maior preço", "além desse"])

        # lógica para "mais caro"
        if asking_for_dearer and last_prod_price is not None:
            # produtos com preço MAIOR que o último
            dearer_candidates = [p for p in candidates if p['preco'] > last_prod_price]
            if dearer_candidates:
                # pega o MAIS BARATO entre os MAIS CAROS (próximo acima)
                best = min(dearer_candidates, key=lambda x: x['preco'])
                response = f"🔝 Sim, dentro do seu orçamento existe o **{best['nome']}** por R$ {best['preco']:.2f}. Ele é mais caro que o **{last_prod_name}** e oferece {PRODUCT_DETAILS.get(best['nome'], {}).get('descricao_longa', 'excelentes funcionalidades')}. Gostaria de saber mais?"
            else:
                # informa o mais caro disponível
                most_expensive = max(candidates, key=lambda x: x['preco'])
                response = f"💰 Dentro do orçamento de R$ {budget:.2f}, o produto mais caro é o **{most_expensive['nome']}** (R$ {most_expensive['preco']:.2f}). Não há produtos mais caros que isso dentro do seu limite. Gostaria de ver opções mais baratas ou aumentar o orçamento?"
                best = most_expensive

        elif asking_for_cheaper and last_prod_price is not None:
            cheaper_candidates = [p for p in candidates if p['preco'] < last_prod_price]
            if cheaper_candidates:
                best = max(cheaper_candidates, key=lambda x: x['preco'])
                response = f"📉 Sim, dentro do seu orçamento existe o **{best['nome']}** por R$ {best['preco']:.2f}. É uma opção mais econômica que o **{last_prod_name}**. Deseja mais detalhes?"
            else:
                cheapest = min(candidates, key=lambda x: x['preco'])
                response = f"📉 O **{last_prod_name}** (R$ {last_prod_price:.2f}) já é o produto mais barato dentro do seu orçamento. Gostaria de ver produtos mais caros?"
                best = cheapest

        else:
            # recomendação padrão
            if budget:
                best = max(candidates, key=lambda x: (PRODUCT_DETAILS.get(x['nome'], {}).get('popularidade', 0), x['preco']))
            else:
                best = max(products, key=lambda x: PRODUCT_DETAILS.get(x['nome'], {}).get('popularidade', 0))
            response = f"✅ Recomendo o **{best['nome']}** por R$ {best['preco']:.2f}. {PRODUCT_DETAILS.get(best['nome'], {}).get('descricao_longa', 'Ótima escolha.')} Quer mais informações?"

        self.memory.add_interaction(user_query, response)
        self.memory.last_recommended = best['nome']
        self.memory.last_recommended_price = best['preco']
        return response

    def clear_memory(self):
        self.memory = ConversationalMemory()
        logger.info("🧠 Memória reiniciada")


ai_service = AIService()