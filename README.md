# Suzano-Challenge

O "Suzano-Challenge" é um projeto de chatbot desenvolvido em Python, com o objetivo de responder a perguntas escolares. A ideia principal é que ele busque respostas a partir de um arquivo JSON. Caso a pergunta não esteja lá, o chatbot recorre à API de IA do Gemini para tentar fornecer uma resposta mais precisa e relevante. Além disso, o sistema mantém um histórico das interações, o que facilita a revisão das conversas passadas. Para garantir a segurança, as chaves da API e outros dados sensíveis são armazenados de forma segura usando variáveis de ambiente.

## Funcionalidades

1. **Respostas com base em JSON**: O chatbot consulta um arquivo JSON para responder a perguntas, oferecendo uma maneira rápida e eficaz de lidar com as questões mais comuns.
2. **Integração com a API Gemini**: Quando não há uma resposta no arquivo JSON, o chatbot utiliza a API do Gemini para buscar uma resposta mais contextualizada e precisa.
3. **Histórico de interações**: O sistema armazena todas as perguntas e respostas, permitindo acompanhar facilmente as interações e melhorar o entendimento das conversas.
4. **Segurança**: As chaves de API e outros dados confidenciais são mantidos seguros por meio do uso de um arquivo `.env`, seguindo boas práticas de segurança.

## Tecnologias Utilizadas

- **Python**: A principal linguagem usada no desenvolvimento do projeto.
- **API Gemini**: Usada para complementar as respostas do chatbot quando necessário.
- **POO (Programação Orientada a Objetos)**: Estrutura de código utilizada para tornar o projeto mais modular e reutilizável.
- **.env**: Para garantir que informações sensíveis, como as chaves de API, sejam mantidas em segurança.

## Estrutura do projeto

```json
Suzano-Challenge {
    "data": {
        "perguntas_escolares_com_respostas.json"
    },
    "files": {
        "history": {
            "chat_history_4373.json"
        },
        "chatbot.py"
    }
}