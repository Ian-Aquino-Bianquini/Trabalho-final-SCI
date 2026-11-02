Ian de Aquino Bianquini
Luísa Gama Pina

Sistemas Computacionais Inteligentes

## Como iniciar o projeto

Este projeto recebe a descrição de um problema de manutenção e sugere o setor responsável. O programa roda no seu computador e você utiliza uma página no navegador para fazer as consultas.

### Pré-requisitos

- Um computador com Python 3.10 ou mais recente instalado.
- Um navegador, como Google Chrome, Microsoft Edge ou Firefox.
- A pasta completa do projeto, incluindo a pasta `dados`.

O VS Code é opcional, mas facilita abrir a pasta e executar o programa. Não é necessário instalar bibliotecas extras, criar conta em um serviço de IA ou configurar uma chave de API. Depois de baixar o projeto e instalar o Python, o programa funciona sem internet.

### 1. Instalar o Python

Se você já possui o Python instalado, pode ir para o próximo passo.

1. Acesse o [site oficial do Python](https://www.python.org/downloads/windows/).
2. Baixe e instale uma versão estável do Python 3.10 ou mais recente para Windows.
3. Se o instalador apresentar a opção **Add python.exe to PATH**, marque essa opção. Ela permite executar o Python pelo terminal.
4. Conclua a instalação. Se o VS Code estiver aberto, feche e abra novamente para que ele reconheça o Python.

### 2. Abrir o terminal e conferir o Python

O terminal é a área onde você digita os comandos para iniciar o programa.

1. No VS Code, clique em **Terminal > Novo Terminal** ou **Terminal > New Terminal**.
2. Na área que abrir na parte inferior da janela, digite o comando abaixo e pressione **Enter**:

```powershell
python --version
```

Deve aparecer uma versão como `Python 3.12.0`. O número pode ser diferente, desde que seja 3.10 ou mais recente.

Se o comando não funcionar, tente:

```powershell
py --version
```

### 3. Iniciar o programa

Utilize `py` ou `python`, tente o `py` e caso de erro tente o `python`, ambos os comandos executam corretamente.

No mesmo terminal, digite e pressione **Enter**:

```powershell
python app.py
```

Execute apenas uma das opções. O terminal deve mostrar uma mensagem parecida com esta:

```text
Triagem disponível em http://127.0.0.1:8000. Para encerrar, pressione Ctrl+C.
```

O navegador deve abrir automaticamente. Se isso não acontecer, abra o navegador e digite **http://127.0.0.1:8000** na barra de endereços.

Esse endereço abre o programa no seu próprio computador. Mantenha o terminal aberto enquanto estiver usando a página. Não abra `pagina.html` diretamente: a página precisa se comunicar com o programa iniciado pelo comando acima.

### 4. Fazer uma consulta

1. No campo **O que aconteceu?**, escreva uma descrição, por exemplo: `A torneira do banheiro está vazando`.
2. Clique em **Sugerir setor**.
3. O programa deve mostrar **Manutenção hidráulica** e os termos conhecidos que entraram no cálculo.
4. Para fazer outra consulta, substitua o texto e clique no botão novamente.

O resultado é uma sugestão e precisa de conferência. O programa não registra um chamado nem aciona uma equipe de manutenção.