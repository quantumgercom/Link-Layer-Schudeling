# **Estratégia de Agendamento de Purificação Híbrida para Redes Quânticas de Canais Ruidosos Heterogêneos**

A evolução da Internet Quântica depende da geração eficiente e purificação de pares entrelaçados (EPR) em canais quânticos ruidosos e heterogêneos. No entanto, diversos desafios surgem nesse contexto, como estimar o número ótimo de rodadas de purificação sem conhecimento prévio do tipo de erro do canal, a baixa probabilidade agregada de sucesso nos processos de purificação e o desperdício de recursos causado pelos pares EPR não utilizados. Neste trabalho, propomos uma **Estratégia Híbrida de Agendamento de Purificação** em redes quânticas para lidar com esses desafios. Nossa abordagem ajusta dinamicamente o número de rodadas de purificação, compensa a baixa probabilidade de sucesso por meio de operações adicionais e reduz as ineficiências no uso de recursos ao reutilizar pares EPR ociosos. Avaliamos a solução por meio de estudos de caso em cenários de ruído, incluindo os modelos **bit-flip, Werner e ruído misto**. Os resultados demonstram melhorias significativas no throughput e na eficiência de recursos em comparação com abordagens estáticas, destacando a eficácia da estratégia de agendamento dinâmico em redes quânticas reais.

---

## Diretórios
- **quantumnet**:
  - `/components`: Arquivos básicos para o realização das simulações.
  - `/layers`: Arquivos que contêm as camadas para o funcionamento básico da rede.
  - `/objects`: Elementos essenciais para o funcionamento dos componentes.

## **Camada de Enlace**

A **camada de enlace** é responsável pelo gerenciamento da comunicação direta entre os nós da rede, garantindo a criação, manutenção e qualidade dos **pares de emaranhamento quântico (EPRs)** entre os hosts conectados. Ela atua como um intermediário essencial entre a **camada física**, que realiza a geração dos qubits e pares emaranhados, e as camadas superiores da pilha de rede quântica, que utilizam esses recursos para operações mais complexas, como teletransporte de qubits e protocolos de computação segura.

### **Principais Funções da Camada de Enlace**
1. **Solicitação de Emaranhamento**  
   - A camada recebe solicitações de pares de hosts (ex: Alice e Bob) para estabelecer emaranhamento.
   - Coordena com a camada física para tentar criar esses pares usando protocolos de criação de emaranhamento com heralding.

2. **Gerenciamento de Recursos**  
   - Mantém um controle detalhado sobre os **EPRs utilizados e criados** durante as operações.
   - Monitora a taxa de sucesso das solicitações e gerencia tentativas de reestabelecimento em caso de falhas.

3. **Purificação de EPRs**  
   - Implementa **diferentes protocolos de purificação**, como **symmetric e pumping**, para melhorar a **fidelidade dos pares EPRs**.
   - Suporta estratégias avançadas, incluindo **purificação auxiliar e múltiplas tentativas** para aumentar a confiabilidade da conexão.
   - Realiza a purificação em **múltiplos rounds**, garantindo que os pares de EPRs atinjam fidelidades adequadas para aplicações superiores.

4. **Agendamento de Purificação**  
   - Planeja quando e quantas vezes a purificação deve ser executada para maximizar o desempenho.
   - Verifica **se há EPRs suficientes** para a execução da purificação e, se necessário, solicita novos pares à camada física.

5. **Cálculo de Fidelidade e Estimativas de Recursos**  
   - Mede a fidelidade média dos EPRs disponíveis na camada.
   - Estima a quantidade necessária de **rounds de purificação** e **pares EPRs de base** para atingir uma fidelidade-alvo.
   - Ajusta a estratégia de purificação conforme as **características do canal**, considerando fatores como erro e decoerência.

6. **Registro e Depuração**  
   - Mantém logs detalhados sobre as operações, incluindo tentativas de emaranhamento, purificação e falhas.
   - Oferece visibilidade sobre o consumo e criação de EPRs, permitindo otimizações na alocação de recursos.

---

## **Classe `Network`**

A classe **`Network`** representa a infraestrutura principal da **rede quântica**, atuando como o núcleo que **gerencia a comunicação** entre os hosts e coordena as diversas **camadas da pilha de rede quântica**.  

### **Principais Responsabilidades**  

1. **Estrutura e Topologia da Rede**  
   - Utiliza um grafo (`networkx.Graph`) para modelar os **nós (hosts)** e **arestas (canais quânticos)** da rede.  
   - Permite a criação de topologias padrão, como **grade, linha e anel**.  

2. **Gerenciamento de Camadas**  
   - Implementa e interliga as camadas **física, enlace, rede, transporte e aplicação**.  
   - Cada camada possui funções especializadas para manipular **qubits, pares EPRs e pacotes de comunicação**.  

3. **Gerenciamento de Hosts e Conectividade**  
   - Permite adicionar hosts à rede e estabelecer conexões.  
   - Mantém um dicionário de **hosts ativos** e suas conexões.  

4. **Gestão de EPRs e Qubits**  
   - Controla a criação, armazenamento e consumo de **pares EPRs** nos canais da rede.  
   - Implementa **métricas de fidelidade** e **políticas de purificação** para otimizar a qualidade da comunicação.  

5. **Manutenção do Estado da Rede**  
   - Controla **timeslots**, permitindo a evolução do estado da rede e aplicando **decoerência** aos qubits.  
   - Mantém registros detalhados de **EPRs usados, qubits consumidos e métricas gerais** da simulação.  

6. **Métricas e Relatórios**  
   - Coleta estatísticas sobre a utilização da rede, como **total de EPRs e qubits utilizados, fidelidade média e eficiência das rotas**.  
   - Permite exportar as métricas em **CSV**, exibi-las no console ou armazená-las em variáveis para análise posterior.  

---

## **Camada Física (`PhysicalLayer`)**

A **camada física** é a base da pilha de rede quântica, responsável por **criar, manipular e medir qubits e pares entrelaçados (EPRs)**. Essa camada interage diretamente com os dispositivos físicos da rede e **simula a geração e degradação dos qubits** ao longo do tempo, considerando efeitos como **decoerência** e **ruído nos canais de comunicação**.

### **Principais Responsabilidades da Camada Física**

1. **Geração e Gerenciamento de Qubits**  
   - **Criação de qubits** nos hosts da rede e atribuição a uma **memória quântica**.  
   - Registro da fidelidade inicial de cada qubit e acompanhamento de sua degradação ao longo dos **timeslots**.  
   - Mede a fidelidade dos qubits e aplica fatores de **decoerência** para simular os efeitos da física real.  

2. **Criação e Gerenciamento de Pares EPRs**  
   - Cria **pares de qubits entrelaçados** (EPRs) que podem ser usados para **teletransporte quântico** e **distribuição de chaves quânticas (QKD)**.  
   - Monitora **tentativas falhas de criação de EPRs**, armazenando pares defeituosos para análise e possível purificação em camadas superiores.  
   - Gerencia a **fidelidade dos EPRs**, garantindo que os pares sejam **adicionados aos canais de comunicação** caso atendam aos critérios mínimos de fidelidade.  

3. **Protocolos de Criação de Emaranhamento**  
   - **Entanglement Creation Heralding Protocol (ECHP)**  
     - Método baseado em **sinalização**, onde dois qubits são medidos após tentativas de emaranhamento.  
     - Caso a fidelidade seja suficiente, um **par EPR válido** é adicionado à rede. Se falhar, o EPR é armazenado como **EPR defeituoso**.  

4. **Interação com a Rede e Outros Elementos**  
   - **Adiciona e remove EPRs** dos canais da rede, permitindo que outras camadas utilizem esses recursos para comunicação.  
   - Mantém registros detalhados de **qubits criados, usados e descartados**, permitindo que métricas sejam extraídas e analisadas.  


### Como Realizar os Testes  

Os testes são realizados executando múltiplas simulações utilizando os arquivos **[script.py](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/Script.py)** e [loop_para_simulação.ipynb](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/loop%20para%20simula%C3%A7%C3%A3o.ipynb). O primeiro arquivo configura a simulação de purificação de EPRs em uma rede quântica, enquanto o segundo realiza um loop para rodar **100 tentativas*, coletando métricas e analisando o desempenho do agendamento de purificação.

---

## *1. Estrutura dos Arquivos*  

### **Arquivo [script.py](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/Script.py)**  

Este script é responsável por:  
✔ Inicializar a rede quântica e configurar a *topologia*  
✔ Criar hosts e definir a *fidelidade inicial* dos pares EPR  
✔ Escolher o *tipo de canal* e *tipo de purificação*  
✔ Estimar o número necessário de *rounds de purificação*  
✔ Executar o *agendamento de purificação* e verificar o sucesso  
✔ Registrar as métricas no *arquivo CSV*  

**Passo a passo do [script.py](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/Script.py):**  
1. Importa as bibliotecas necessárias, configura os caminhos e ativa o Logger  
2. Inicializa a rede (Network()) e define a *topologia "Grade"*  
3. Ajusta a *fidelidade inicial* dos pares EPR  
4. Define os hosts (Alice e Bob) e coleta informações sobre o *canal quântico*  
5. Define *request de fidelidade alvo* e verifica se pode ser atingida  
6. Seleciona o *tipo de purificação* e estima os *rounds necessários*  
7. Executa a *purificação* e coleta os resultados  
8. Registra as métricas da camada de enlace no *arquivo CSV*  
9. Imprime os resultados da simulação em *JSON*  

---

### **Arquivo [loop_para_simulação.ipynb](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/loop%20para%20simula%C3%A7%C3%A3o.ipynb)**  

Este notebook executa o script [script.py](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/Script.py) em um loop para *100 tentativas*, coletando dados e analisando estatísticas.  

*Principais funções do loop:*  
✔ *Executa o script* script.py repetidamente usando subprocess  
✔ *Filtra e analisa os resultados JSON* de cada simulação  
✔ *Registra as métricas no CSV* e evita duplicações  
✔ *Renumera as simulações no CSV* para manter uma numeração sequencial  
✔ *Acumula métricas* como número total de EPRs criados, consumidos e fidelidade média  
✔ *Gera um resumo estatístico, incluindo **taxas de sucesso e falha*  

**Passo a passo do [loop_para_simulação.ipynb](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/loop%20para%20simula%C3%A7%C3%A3o.ipynb):**  
1. *Limpa o CSV* anterior, se existir  
2. *Executa 100 simulações*, capturando saídas JSON  
3. *Filtra as simulações ignoradas* (exemplo: canais não suportados)  
4. *Verifica o sucesso ou falha* da purificação e registra métricas  
5. *Renumera as simulações no CSV* para manter um histórico correto  
6. *Calcula métricas acumuladas* e exibe um *resumo final*  

---

## *2. Como Executar os Testes*  

### **Opção 1: Rodar o script.py individualmente**  
Executa uma simulação única com os parâmetros padrão:  
```bash
python script.py
```


### *Opção 2: Rodar o loop de 100 tentativas no Jupyter Notebook*  
Abrir o *Jupyter Notebook* e rodar o loop_para_simulação.ipynb. Isso executará 100 simulações, coletando métricas e gerando um **resumo estatístico**.

### *Opção 3: Executar o loop via terminal*  
Caso prefira rodar tudo via terminal, pode-se usar:  
```bash
jupyter nbconvert --to script loop_para_simulação.ipynb && python loop_para_simulação.py
```
Isso converterá o notebook em um script Python e o executará automaticamente.

---

## *3. Analisando os Resultados*  

Após a execução do loop para simulação.ipynb, as métricas serão exibidas no terminal e salvas no arquivo **link_metrics_output.csv**.  

### *Resumo Estatístico Final*
✔ *Total de Timeslots Utilizados*  
✔ *Total de EPRs Criados e Consumidos*  
✔ *Fidelidade Média Total*  
✔ *Número de Simulações Bem-Sucedidas e com Erro*  
✔ *Porcentagem de Sucesso e Falha*  

No terminal, será exibido algo como:  
```plaintext
Resumo das Métricas da Simulação:
Total de Timeslots: 2345
Total de EPRs Criados: 1500
Total de EPRs Consumidos: 1350
Fidelidade Média Total: 0.87

A quantidade de simulações que deu certo é 300
As simulações que deram certo foram [1, 2, 4, 7, 10, 15, ...]

A quantidade de simulações que falharam é 150
As simulações que falharam foram [3, 5, 6, 8, 9, 11, ...]

A porcentagem de simulações bem-sucedidas é 66.67%
A porcentagem de simulações com erro é 33.33%
````
---

## *4. Modificações e Personalizações*  

Se desejar modificar os testes, pode-se:  
✔ Alterar *o tipo de purificação* (pumping, symmetric, etc.)  
✔ Mudar a *request de fidelidade alvo*  
✔ Ajustar o *número de tentativas* no loop  
✔ Habilitar *mais tipos de canais* para teste  

---


## Ambiente de Testes  
A ferramenta foi executada e testada na prática nos seguintes ambientes:  

1. **Windows 11**  
   - Kernel: 10.0.22621  
   - Python: 3.12.0  
   - Módulos Python conforme [requirements.txt](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/requirements.txt)  

2. **Ubuntu 12 LTS**  
   - Kernel Version: 6.1.0-30-amd64  
   - Python Version: 3.11.2  
   - Módulos Python conforme [requirements.txt](https://github.com/quantumgercom/Link-Layer-Schudeling/blob/main/requirements.txt)  


## Instruções de instalação
1. Clonar o repositório

   ```
   $ git clone https://github.com/quantumgercom/Link-Layer-Schudeling.git
   ```
3. Instalar as dependências
   
   As principais ferramentas utilizadas são:
`Matplotlib`, `Networkx`, além do `Jupyter Notebook`. Para obtê-las, utiliza-se o `pip`. Isso pode ser feito individualmente, ou por meio do arquivo `requiriments.txt` deste repositório com o seguinte comando no terminal:
   ```
   $ pip install -r requirements.txt
   ```
   Este documento contém todas as dependências utilizadas pelo ambiente virtual onde o código foi desenvolvimento.
5. Pronto

   Após clonar o repositório e instalar as dependências, os notebooks e o restante dos códigos já podem ser executados e manipualdos.
   
---

Este conjunto foi desenvolvido como parte de um artigo em revisão para o SBRC 2025, visando avanços na simulação e gestão de redes quânticas de alta confiabilidade.

Essas funcionalidades permitem que a camada de enlace gerencie de forma eficiente o emaranhamento e as operações de purificação, assegurando uma comunicação quântica confiável e de alta fidelidade entre os nós da rede.
