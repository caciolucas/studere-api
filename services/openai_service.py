import openai

from core.exceptions import OpenAIAPIError


class OpenAIService:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """
        Inicializa o cliente para a API OpenAI.

        Parâmetros:
            api_key (str): Sua chave de API da OpenAI.
            model (str): O modelo a ser usado (padrão é 'gpt-4-turbo').
            temperature (float): Controla a aleatoriedade da resposta.
            max_tokens (int): Número máximo de tokens para a resposta.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = openai.OpenAI(api_key=api_key)

    def create_prompt(self, prompt: str) -> dict:
        """
        Cria a estrutura de payload para a solicitação.

        Parâmetros:
            prompt (str): A entrada do usuário para o modelo.

        Retorno:
            dict: O payload estruturado para a solicitação.
        """
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

    def get_response(self, prompt: str) -> str:
        """
        Envia a solicitação para a API OpenAI e retorna a resposta.

        Parâmetros:
            prompt (str): A entrada do usuário para o modelo.

        Retorno:
            str: O texto da resposta gerada pelo modelo.
        """
        payload = self.create_prompt(prompt)
        try:
            response = self.client.chat.completions.create(**payload)
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise OpenAIAPIError(
                f"OpenAI API error: {e}"
            )
