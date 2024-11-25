from decouple import config

DEFAULT_PROMPT = """
Baseada na descrição informada, retorne um json no formato abaixo que representará um plano de estudo para os assuntos definidos na descrição:
[{{
   "title": "Task name",
   "topics": [
      {{
         "title": "Task activity name",
         "description": "Description of this task",
      }}
   ]
}}]

{}


NÃO RETORNE EM MARKDOWN, RETORNE PURAMENTE O JSON A SER PARSEADO
O RETORNO DEVE SER SOMENTE O JSON COM O CONTEÚDO, NÃO RETORNE NADA ALÉM DO JSON, NENHUM OUTRO CONTEÚDO
"""

OPEN_AI_KEY: str = config("OPEN_AI_KEY")
