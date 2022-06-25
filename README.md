# Relatório completo
  Caso seja necessário mais informações, tem um pdf chamado `GustavoValenteRelatorio.pdf` com as informações detalhadas da implementação do trabalho em formato de artigo acadêmico.

# Introdução
  O leiame é referente ao trabalho da disciplina de otimização. Nesse trabalho foi feito uma pesquisa em cima do problema de envio de cargas. Desde a criação da modelagem do problema em forma de programação linear, até encontrar a sua solução.

# Estrutura de diretórios:
  src: Contém o código fonte. <br/>
    main.py: Contém a modelagem do problema utilizando o python versão 3.10.0 <br/>
  teste: Contém os arquivos utilizados para testes. <br/>
  Makefile: Arquivo que contém o makefile. <br/>
  parcial-relaxada-relatorio.pdf: Contém o relatório de tudo que foi feito. <br/>


# Forma de reproduzir o código:
  basta digitar para instalar todas as dependências do projeto: <br/>
  pip3 install ortools (dependência) <br/>
  
  Para executar o algoritimo: <br/>
    make <br/>
    ./parcial-relaxada < entrada.in <br/>

  ou, é possível criar um arquivo de teste e colocar dentro do diretório ./tests/ e digitar: <br/>
    make <br/>
    make run <br/>

  Assim o makefile vai executar todos os testes dentro de ./testes/, e vai jogar o output dentro de uma saída padrão.<br/>


# Notas:
  Caso exista algum problema para se reproduzir o projeto em alguma máquina, verificar a versão em que se está o python3 e também verificar se na primeira lina do arquivo src/main.py, onde fica o #!/usr/bin/python3 se está de acordo com o path do seu python caso não esteja, basta mudar essa linha de acordo e compilar o código novamente com o comando make.
