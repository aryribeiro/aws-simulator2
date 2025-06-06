Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print](https://github.com/user-attachments/assets/22fde294-0bbc-45b9-9d03-9dc1aa32d629)

# 📝 AWS Simulator CCP

Simulador para a certificação **AWS Certified Cloud Practitioner (CCP)** 2025, com interface web intuitiva e sistema de perguntas dinâmico.

## 🎯 Sobre o Projeto

Este simulador foi originalmente desenvolvido para a certificação AWS Solutions Architect Associate (SAA-C03) e foi adaptado para a certificação AWS Cloud Practitioner (CCP), mantendo toda a robustez e funcionalidades do web app original.

### ✨ Características Principais

- **65 questões** abrangendo todos os domínios da certificação CCP
- **Timer de 130 minutos** (2h10min) simulando condições reais do exame
- **Suporte a múltipla escolha** e questões de seleção única
- **Carregamento dinâmico** de perguntas via Google Drive CSV
- **Interface limpa e responsiva** otimizada para foco máximo
- **Feedback instantâneo** com marcação de questões incorretas
- **Sistema de pontuação** com porcentagem de acertos

## 🚀 Funcionalidades

### Para Candidatos:
- ⏱️ **Timer realístico** com contagem regressiva
- 📊 **Métricas de performance** ao final do simulado
- ✅ **Marcação visual** de questões corretas/incorretas
- 🔒 **Bloqueio de alterações** após finalização
- 📱 **Design responsivo** para desktop e mobile

### Para Administradores:
- ➕ **Adicionar novas questões** via interface web
- 🗑️ **Remover questões** desnecessárias
- 📝 **Gerenciar banco de questões** de forma intuitiva
- 🔄 **Atualização dinâmica** via Google Drive

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework principal para interface web
- **Pandas** - Manipulação e análise de dados
- **Requests** - Comunicação com APIs externas
- **Python-dotenv** - Gerenciamento de variáveis de ambiente
- **Google Drive** - Armazenamento e sincronização de questões

## 📋 Pré-requisitos

- Python 3.8+
- Pip (gerenciador de pacotes Python)
- Conta Google Drive (para hospedagem do CSV)

## 🔧 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/aryribeiro/aws-simulator2.git
cd aws-simulator2
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
# Crie o arquivo .env na raiz do projeto
echo "GOOGLE_DRIVE_CSV_URL=https://drive.google.com/uc?export=download&id=SEU_FILE_ID" > .env
```

4. **Execute o simulador:**
```bash
streamlit run app.py
```

5. **Execute o gerenciador de questões (opcional):**
```bash
streamlit run manage_questions.py
```

## 📊 Estrutura do Projeto

```
aws-ccp-simulator/
├── app.py                 # Aplicação principal do simulador
├── manage_questions.py    # Interface de gerenciamento de questões
├── questions.csv          # Banco local de questões (backup)
├── .env                   # Variáveis de ambiente
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 📁 Formato do CSV de Questões

O arquivo CSV deve conter as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `question` | Texto da pergunta | "Qual serviço AWS oferece armazenamento de objetos?" |
| `options` | Lista de opções | `["Amazon S3", "Amazon EBS", "Amazon EFS", "Amazon FSx"]` |
| `answer` | Resposta(s) correta(s) | `["Amazon S3"]` |
| `multiple` | Permite múltiplas respostas | `false` |

### Exemplo de linha no CSV:
```csv
question,options,answer,multiple
"Qual é o modelo de precificação do Amazon S3?","[""Pay-as-you-go"", ""Flat rate"", ""Subscription"", ""Free tier only""]","[""Pay-as-you-go""]",false
```

## 🎓 Domínios Cobertos (AWS CCP)

1. **Conceitos de Nuvem (26%)**
   - Definir a Nuvem AWS e sua proposta de valor
   - Identificar aspectos da economia da nuvem
   - Listar os diferentes princípios de design de arquitetura de nuvem

2. **Segurança e Conformidade (25%)**
   - Definir o modelo de responsabilidade compartilhada da AWS
   - Definir conceitos de segurança e conformidade na nuvem AWS
   - Identificar recursos de gerenciamento de acesso da AWS

3. **Tecnologia (33%)**
   - Definir métodos de implantação e operação na Nuvem AWS
   - Definir a infraestrutura global da AWS
   - Identificar os principais serviços da AWS

4. **Cobrança e Preços (16%)**
   - Comparar e contrastar os vários modelos de preço da AWS
   - Reconhecer as várias estruturas de conta em relação à cobrança e preços da AWS
   - Identificar recursos disponíveis para suporte de cobrança

## 🎯 Como Usar

### Realizando um Simulado:

1. Acesse a aplicação via browser
2. Clique em **"Iniciar Simulado"**
3. Responda todas as 65 questões
4. Monitore o timer no canto superior direito
5. Clique em **"Finalizar Simulado"** quando terminar
6. Analise seus resultados e questões incorretas

### Gerenciando Questões:

1. Execute `streamlit run manage_questions.py`
2. Use o formulário para adicionar novas questões
3. Visualize e remova questões existentes
4. As alterações são salvas automaticamente

## 📈 Métricas de Aprovação

- **Nota mínima:** 70% (700 pontos de 1000)
- **Total de questões:** 65 questões
- **Tempo disponível:** 130 minutos
- **Aprovação no simulador:** 46 questões corretas ou mais

## 🔄 Atualizações e Manutenção

### Histórico de Versões:
- **v2.0.0** - Adaptação para AWS Cloud Practitioner (CCP)
- **v1.0.0** - Versão original para AWS Solutions Architect Associate (SAA-C03)

### Adicionando Novas Questões:
1. Utilize o `manage_questions.py` para interface gráfica
2. Ou edite diretamente o CSV no Google Drive
3. As questões são carregadas automaticamente no próximo acesso

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Ary Ribeiro**
- Email: aryribeiro@gmail.com
- Certificado AWS Solutions Architect Associate
- Especialista em Cloud Computing

## 🆘 Suporte

### Problemas Comuns:

**Erro ao carregar questões:**
- Verifique se a URL do Google Drive está correta no arquivo `.env`
- Certifique-se de que o arquivo CSV está publicamente acessível

**Timer não funciona:**
- Atualize a página (F5)
- Verifique se o JavaScript está habilitado no browser

**Questões não salvam:**
- Verifique as permissões de escrita no diretório
- Confirme se o arquivo `questions.csv` existe

### Para mais ajuda:
- Abra uma issue no GitHub
- Entre em contato via email: aryribeiro@gmail.com

---

## 🎖️ Sobre a Certificação AWS CCP

A certificação AWS Certified Cloud Practitioner é uma certificação de nível fundamental que valida o conhecimento geral da nuvem AWS. É ideal para:

- Profissionais de negócios não técnicos
- Iniciantes em cloud computing
- Profissionais de TI buscando conhecimento básico em AWS
- Estudantes e recém-formados

**Validade:** 3 anos
**Formato:** 65 questões de múltipla escolha
**Duração:** 130 minutos
**Preço:** USD $100
