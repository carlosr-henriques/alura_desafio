# AluMind (Processo seletivo Alura)

# Contexto

A AluMind é uma startup que oferece um aplicativo focado em bem-estar e saúde mental, proporcionando aos usuários acesso a meditações guiadas, sessões de terapia, e conteúdos educativos sobre saúde mental. Com o alto crescimento da base de usuários, a AluMind está começando a ter gargalos para analisar feedbacks vindo dos usuários em diferentes plataformas (canais de atendimento ao cliente; comunidades no Discord; redes sociais). Portanto, nessa tarefa, você criará uma aplicação cuja responsabilidade seja de analisar os feedbacks vindos dos usuários, classificá-los a partir do seu sentimento e elencar as possíveis melhorias contidas neles.

O projeto consiste de 4 etapas, sendo a última opcional.  

1. Classificação de Feedbacks: Criar um endpoint que receba os feedbacks em uma estrutura JSON, e classificá-los utilizando um LLM. Cada feedback precisa ser marcado com o sentimento **POSITIVO**, **NEGATIVO** ou **INCONCLUSIVO**. Também é necessário identificar as sugestões de novas funcionalidades - feitas pelos usuários que apresentaram feedback -, através de um código e descrição da funcionalidade solicitada.  
2. Relatório Web: Disponibilizar uma página com informações sobre os feedbacks.  
3. Resumo semanal: Um email contendo informações estatísticas dos feedbacks, principais funcionalidades pedidas e o porquê cada uma seria importante. O uso de uma LLM para a geração do email é opcional.
4. (Bônus não obrigatório) Filtro de feedback: Implementação de um sistema de filtragem no endpoint de envio de feedbacks que assegure que apenas feedbacks legítimos e não classificados como spam sejam processados e armazenados.

# Melhorias mapeadas para futuras versões

1. Página de indicadores de tokens, custo, quantidade de feedbacks recebidos no método POST, quantidade de feedbacks classificados como ilegítimo pelo filtro da tarefa bônus.  
2. Uma lógica para armazenar mais de uma classificação e sugestão de funcionalidade que o LLM fizer para um único feedback. Atualmente, a solução pega o primeiro feedback classificado.  
3. Melhorar o visual da página de relatórios, apresentando informações gráficas diversas (atualmente é exibido somente tabelas).  
4. Testagem de novos prompts de instrução mais otimizados que garantam os mesmos resultados. Técnicas de prompt engineering e LangChain são opções mais aderentes para a melhoria.  
5. Testagem de novos prompts ou do mesmo prompt que gera o email enviado aos stackholders.
6. Utilizar uma única solução de conexão com o bancos de dados. A solução usando somente ORM (SQLAlchemy) possibilitará maior legibilidade do código, e menos tempo de manutenções e melhorias.  
7. Usar o processo de envio de email em uma página web (usando Flask-Mail), para manter todas as soluções integradas em um único local. Atualmente o código utiliza pacotes padrão da linguagem Python.
8. Testar novos prompts para a filtragem dos feedbacks. A solução atual (arquivo app_com_bonus.py não pode ser utilizada, uma vez que ao testar o prompt, feedbacks legítimos de serem classificados, foram classificados como ilegítimos, impossibilitanto seu processamento e armazenamento).
9. Filtrar os feedbacks da semana anterior, e assim computar as informações corretas para o envio do email aos Stackholders.
10. Implementação do framework LangChain para melhorar os prompts, saídas dos modelos, otimização das respostas através de classes que permitam gerar respostas mapeadas em cache e através de SGBD ou bases de dados baseado em vetores.  

# Insights iniciais

1. O LLM precisará de um contexto (parâmetro system_instruction) que permita entender seu propósito a cada chamada do método POST da API. Isso permite reduzir o tamanho do prompt e sua quantidade de tokens computados.
2. Toda solução é desenvolvida em funções e módulos, separando os propósitos de cada módulo e separando as tarefas em funções, permitindo a reutilização de código
3. Informações sigilosas como chave de API, credenciais de bancos de dados e outras informações são acessadas usando variável de ambiente (definidas no arquivo .env)

# LLM

O modelo escolhido para o case foi o Gemini 1.5 Flash. Esse modelo permite alcançar qualidade comparável a modelos maiores, por uma fração do custo e com uma latência média abaixo de um segundo para a grande maioria dos casos. Por ser um modelo multimodal, não implica em migração de modelos que suportem outras estruturas de dados como Imagem e Vídeos, uma vez que estas estruturas são suportadas. A principal característica favorável para a escolha deste modelo é a sua velocidade. Mais informações podem ser visualizadas no site da DeepMind, [clicando aqui](https://deepmind.google/technologies/gemini/flash/?hl=pt-br). Os benchmarks comparando com outros modelos, mostram que o Flash perde somente para a versão Pro.

# Conclusão

A solução desenvolvida permite a análise de feedback feita pelos usuários da AluMind, armazenamento dos feedbacks analisados, visão analítica sobre os feedbacks através de uma relatório web e divulgação dos resultados para os stackholders, que poderão identificar as dores ou sugestões dos clientes, a satisfação e insatisfação dos clientes.

# Como executar o projeto

1. Clone o repositório:

```
git clone https://github.com/carlosr-henriques/alura_desafio.git
```

2. Instale as dependências necessárias (recomenda-se utilizar um ambiente virtual). O projeto foi desenvolvido com a versão 3.11.4 do Python:

3. Execute o arquivo **app.py** na sua IDE de preferência e acesse o site localmente através do link disponibilizado pelo miniframework Flask. Para testar o envio dos dados, utilize a solução Thunder Client ou a solução Postman. Ambas precisam ser instaladas na máquina. A solução Thunder Cliente pode ser instalada como uma extensão do VS Code. Para testar o email, basta executar o arquivo **create_email.py**.

**Obs.:**: Foi disponibilizado o arquivo **app_com_bonus.py**, contendo a solução bônus. A solução não está funcionando da forma adequada, porém, foi disponibilizada para avaliação.

   
