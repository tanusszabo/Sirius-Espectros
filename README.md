## Sirius_Espectros: Uma ferramenta Python para análise de espectros de fótons do Sirius

Este pacote Python fornece uma maneira conveniente de carregar, processar, plotar e salvar dados de espectro de fótons, particularmente aqueles provenientes das linhas de luz do Sirius no CNPEM.

### Recursos

- Carregamento de dados de espectro de arquivos de texto.
- Conversão de dados de largura de banda para energia.
- Normalização de dados de espectro por corrente.
- Plotagem de dados de espectro com opções personalizáveis.
- Escrita de dados de espectro processados em arquivos de texto.
- Suporte para unidades comuns de energia e fluxo.

### Instalação

1. Certifique-se de ter o Python 3.6 ou superior instalado.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Uso

1. **Importar a classe Espectros:**
   ```python
   from Sirius_Espectros import Sirius_Espectros
   ```

2. **Criar uma instância da classe:**
   ```python
   espectros = Espectros()
   ```

3. **Carregar dados de espectro de um arquivo:**
   ```python
   data = espectros.get_spectrum_data("caminho/para/arquivo.txt")
   ```

4. **Realizar operações nos dados:**
   - Converter dados de largura de banda para energia:
     ```python
     data = espectros.bandwidth_to_energy(data, energy_u="eV", flux_u="ph/s/0.1%", current=100)
     ```
   - Normalizar dados por corrente:
     ```python
     data = espectros.normalize_spectrum(data, energy_u="eV", flux_u="ph/s/eV", current=100)
     ```

5. **Plotar dados de espectro:**
   ```python
   espectros.plot_spectrum_data(data, energy_u="keV", flux_u="ph/s/eV", current=350, title="Título do Gráfico")
   ```

6. **Salvar dados de espectro processados:**
   ```python
   espectros.write_data_file(data, "nome_do_arquivo.txt")
   ```

### Exemplos

Consulte o arquivo `Sirius_Espectros.py` para exemplos detalhados de como usar as diferentes funções.

### Estrutura de Arquivos

- `Sirius_Espectros/`
    - `Sirius_Espectros.py`: Contém o código-fonte da classe `Espectros`.
    - `requirements.txt`: Lista as dependências do pacote.
    - `spectrum_data/`: Diretório para armazenar arquivos de dados de espectro.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull. Mas já aviso que eu só verei a sua contribuição quando eu estiver sem mais nada pra fazer.

### Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.
