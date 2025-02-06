import json
import os
import requests
import unidecode
import string
import random
from difflib import get_close_matches
from dotenv import load_dotenv

class Chatbot:
    def __init__(self, json_file):
        """
        input: json_file (str)
        output: None
        return: None
        
        Inicializa o chatbot carregando as perguntas e respostas do JSON e definindo as configurações da API.
        """
        self.json_file = json_file
        self.responses = self.load_responses()
        self.history = []
        load_dotenv(os.path.join(os.path.dirname(__file__), "api.env"))
        self.api_key = os.getenv("GEMINI_API_KEY")

    def normalize_text(self, text):
        """
        input: text (str)
        output: None
        return: text (str)
        
        Normaliza um texto removendo acentos, pontuações e transformando em minúsculas.
        """
        text = unidecode.unidecode(text.lower()).strip()
        return text.translate(str.maketrans('', '', string.punctuation))

    def load_responses(self):
        """
        input: None
        output: None
        return: responses (dict) - Dicionário contendo perguntas normalizadas e suas respostas.
        
        Carrega as perguntas e respostas do arquivo JSON e as normaliza para facilitar a busca.
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                responses = {}
                for category, qa_pairs in data.items():
                    for question, answer in qa_pairs:
                        normalized_question = self.normalize_text(question)
                        responses[normalized_question] = answer
                return responses
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def get_fixed_response(self, question):
        """
        input: question (str)
        output: None
        return: response (str | None) - Resposta fixa encontrada no JSON ou None caso não encontrada.
        
        Busca uma resposta fixa no JSON correspondente à pergunta normalizada.
        """
        normalized_question = self.normalize_text(question)
        response = self.responses.get(normalized_question, None)
        
        if response is None:
            closest_match = get_close_matches(normalized_question, self.responses.keys(), n=1, cutoff=0.8)
            if closest_match:
                response = self.responses[closest_match[0]]
        return response

    def get_ai_response(self, question):
        """
        input: question (str)
        output: None
        return: response (str) - Resposta gerada pela API Gemini ou mensagem de erro.
        
        Obtém uma resposta da API Gemini caso a pergunta não tenha resposta fixa no JSON.
        """
        if not self.api_key:
            return "Erro: Chave da API não configurada."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"prompt": question}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("candidates", [{}])[0].get("output", "Sem resposta gerada.")
        return "Erro ao obter resposta da IA."

    def ask(self, question):
        """
        input: question (str)
        output: None
        return: response (str) - Resposta fixa ou gerada pela IA.
        
        Obtém uma resposta para a pergunta, seja fixa do JSON ou gerada pela IA.
        """
        response = self.get_fixed_response(question)
        if response is None:
            response = self.get_ai_response(question)
        self.history.append((question, response))
        return response

    def show_history(self):
        """
        input: None
        output: Print do histórico da conversa e caminho do arquivo salvo.
        return: None
        
        Exibe o histórico da conversa e salva as interações em um arquivo JSON na pasta 'history'.
        """
        history_dir = os.path.join(os.path.dirname(__file__), "history")
        os.makedirs(history_dir, exist_ok=True)
        filename = f"chat_history_{random.randint(1000, 9999)}.json"
        file_path = os.path.join(history_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)
        
        print(f"\nHistórico de Conversa salvo em '{file_path}'")
        for q, r in self.history:
            print(f"Q: {q}\nA: {r}\n")

if __name__ == "__main__":
    chatbot = Chatbot("./Suzano-Chalenge/data/perguntas_escolares_com_respostas.json")
    
    exit_commands = ["sair", "exit", "quit", "adeus", "tchau", "fechar", "obrigado"]
    
    while True:
        user_input = str(input("Você: ")).strip()
        if chatbot.normalize_text(user_input) in exit_commands:
            chatbot.show_history()
            print("Chat encerrado. Até logo!")
            break
        print("Bot:", chatbot.ask(user_input))