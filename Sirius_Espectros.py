import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import simps
import os

class Espectros:
    energy_unit = { 'eV': 1e0,
                   'keV': 1e3,
                   'MeV': 1e6,
                   'GeV': 1e9}
    flux_unit = {'ph/s/eV':      1,
                 'ph/s/0.1%': 1000}
    
    def __init__(self):
        pass

    def get_spectrum_data(self, filename):
        """
        Carrega dados de espectro de um arquivo, se for um arquivo de espectro válido.

        Args:
            filename (str): Caminho para o arquivo de espectro.

        Returns:
            numpy.ndarray: Dados do espectro como um array numpy, 
                            onde a primeira coluna é a energia e a segunda é o fluxo.
                            Retorna None se o arquivo não for um espectro válido.
        """
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            return None

        spectrum_lines = []
        for line in lines:
            if '#' in line: continue
            try:
                spectrum_lines.append([float(l) for l in line.split()])
            except ValueError:
                continue
        
        if spectrum_lines:
            return np.array(spectrum_lines)
        else:
            # print(f"Aviso: Nenhuma linha de dados encontrada em {filename}")
            return None
    
    def plot_spectrum_data(self, datas, energy_u='keV', flux_u='ph/s/eV', current=350, title=None, fileout=None):
        """
        Plota os dados de espectro.

        Args:
            datas (dict): Dicionário com os dados de espectro. A chave é o nome da linha e o valor é o array numpy com os dados.
            energy_u (str, optional): Unidade de energia para o plot. O padrão é 'keV'.
            flux_u (str, optional): Unidade de fluxo para o plot. O padrão é 'ph/s/eV'.
            current (float, optional): Corrente da linha de luz. O padrão é 350.
            title (str, optional): Título do plot. O padrão é None.
            fileout (str, optional): Arquivo png de saída do plot 
        """
        plt.figure(figsize=(8,6))
        # plt.rcParams.update({"font.size":20})
        if title: plt.title(title)
        plt.grid(True)
        # plt.tight_layout()

        plt.xlabel(f'Energy ({energy_u})')
        plt.ylabel(f'Flux ({flux_u}/{current}mA)')
        plt.yscale('log')
        # plt.xscale('log')

        for d in datas:
            data = datas[d]
            energy_data = data[:,0] / self.energy_unit[energy_u]
            flux_ev_data = data[:,1] * self.flux_unit[flux_u]*current
            plt.plot(energy_data, flux_ev_data, '-o', markersize=2, linewidth=1, label=d)
            
        plt.legend()

        if fileout:
            plt.savefig(fileout)
            plt.close()
        else:
            plt.show()


    def bandwidth_to_energy(self, data, energy_u='eV', flux_u='ph/s/0.1%', current=100):
        """
        Converte dados de espectro de largura de banda para energia.

        Args:
            data (numpy.ndarray): Dados do espectro como um array numpy, onde a primeira coluna é a largura de banda e a segunda é o fluxo.
            energy_u (str, optional): Unidade de energia para a conversão. O padrão é 'eV'.
            flux_u (str, optional): Unidade de fluxo para a conversão. O padrão é 'ph/s/0.1%'.
            current (float, optional): Corrente da linha de luz. O padrão é 100.

        Returns:
            numpy.ndarray: Dados do espectro convertidos para energia, onde a primeira coluna é a energia e a segunda é o fluxo.
        """
        energy_data = data[:,0] * self.energy_unit[energy_u]
        flux_ev_data = data[:,1] * self.flux_unit[flux_u] / data[:,0] / current
        data[:,0] = energy_data
        data[:,1] = flux_ev_data
        return data
    
    def normalize_spectrum(self, data, energy_u='eV', flux_u='ph/s/eV', current=100):
        """
        Normaliza os dados do espectro pela corrente.

        Args:
            data (numpy.ndarray): Dados do espectro como um array numpy, onde a primeira coluna é a energia e a segunda é o fluxo.
            energy_u (str, optional): Unidade de energia para a normalização. O padrão é 'eV'.
            flux_u (str, optional): Unidade de fluxo para a normalização. O padrão é 'ph/s/eV'.
            current (float, optional): Corrente da linha de luz. O padrão é 100.

        Returns:
            numpy.ndarray: Dados do espectro normalizados, onde a primeira coluna é a energia e a segunda é o fluxo.
        """
        energy_data = data[:,0] * self.energy_unit[energy_u]
        flux_ev_data = data[:,1] * self.flux_unit[flux_u] / current
        data[:,0] = energy_data
        data[:,1] = flux_ev_data
        return data

    def plot_folder_spectrum(self, folder, spectrum_type='bandwidth', energy_u='eV', flux_u='ph/s/0.1%', current=1, recursive_check=True):
        """
        Carrega e plota dados de espectro de vários arquivos em uma pasta.

        Args:
            filename (str): Caminho para a pasta contendo os arquivos de espectro.
            spectrum_type (str, optional): Tipo de espectro nos arquivos. Pode ser 'bandwidth' ou 'energy'. O padrão é 'bandwidth'.
            energy_u (str, optional): Unidade de energia para a conversão/normalização. O padrão é 'eV'.
            flux_u (str, optional): Unidade de fluxo para a conversão/normalização. O padrão é 'ph/s/0.1%'.
            current (float, optional): Corrente da linha de luz. O padrão é 1.
            recursive_check (bool, optional): flag para verificar se está em recursão, o que evita o plot

        Returns:
            dict: Dicionário de espéctros com chaves sendo o nome do arquivo e o valor sendo os dados do espectro normalizados.
        """
        if not os.path.isdir(folder):
            return
        
        espec = {}
        for file in sorted( os.listdir(folder) ):
            filepath = os.path.join(folder, file)

            if os.path.isdir(filepath):
                # Chama recursivamente para subpastas
                espec.update(self.plot_folder_spectrum(filepath, spectrum_type, energy_u, flux_u, current, recursive_check=False))

            data = self.get_spectrum_data(filepath)
            if data is None: continue

            if spectrum_type == 'bandwidth':
                data = self.bandwidth_to_energy(data, energy_u=energy_u, flux_u=flux_u, current=current)
            else:
                data = self.normalize_spectrum(data, energy_u=energy_u, flux_u=flux_u, current=current)
            # print(sum(data[:,1]))
            espec[file] = data

        if espec and recursive_check:  # Verifica se há espectros para plotar
            self.plot_spectrum_data(espec, title=folder)

        return espec # Retorna os espectros encontrados

    def write_data_file(self, data, filename, energy_u='eV', flux_u='ph/s/eV', current=1, decimal_places=3):
        """
        Escreve os dados do espectro em um arquivo.

        Args:
            data (numpy.ndarray): Dados do espectro como um array numpy, onde a primeira coluna é a energia e a segunda é o fluxo.
            filename (str): Nome do arquivo para salvar os dados.
            energy_u (str, optional): Unidade de energia para a conversão/normalização. O padrão é 'eV'.
            flux_u (str, optional): Unidade de fluxo para a conversão/normalização. O padrão é 'ph/s/eV'.
            current (float, optional): Corrente da linha de luz. O padrão é 1.
            decial_places (int, optional): Casas decimais para a escrita dos valores de energia e fluxo. O padrão é 3
        """
        energy_label = f"#Energy ({energy_u})"
        flux_label = f"Flux ({flux_u}/{current}mA)"
        energy_data = data[:,0] / self.energy_unit[energy_u]
        flux_ev_data = data[:,1] * self.flux_unit[flux_u]*current

        max1 = max( max( [len(f'{en}') for en in energy_data] ), len(energy_label) )
        max2 = max( max( [len(f'{fl}') for fl in flux_ev_data] ), len(flux_label) )

        data_write = [f'{en:>{max1}.{decimal_places}E} {fl:>{max2}.{decimal_places}E}\n' for en, fl in zip(energy_data, flux_ev_data)]
        with open(filename, 'w') as f:
            f.write(f'{energy_label:>{max1}} {flux_label:>{max2}}\n')
            f.writelines(data_write)

    def integrate_spectrum(self, data, energy_u='eV', flux_u='ph/s/eV', current=100):
        energy_data = data[:,0] * self.energy_unit[energy_u]
        flux_ev_data = data[:,1] * self.flux_unit[flux_u] / current
        integrated_spectrum = simps(y=flux_ev_data, x=energy_data)
        return integrated_spectrum
    
    def integrate_discrete(self, data, flux_u='ph/s/eV', current=100):
        flux_ev_data = data[:,1] * self.flux_unit[flux_u] / current
        integrated_spectrum = sum(flux_ev_data)
        return integrated_spectrum

        

if __name__ == '__main__':
    # EXEMPLO DE USO
    # --------------------------------
    # Plotar comparativos de espectros
    # --------------------------------
    espectros = Espectros()
    espec = {}

    # Carregar dados de um arquivo
    file = 'spectrum_data/Sabia/OPT/undulator/eV/SABIA_flux_B_1p193372_T_eV.txt'
    data = espectros.get_spectrum_data(file)
    # Normalizar dados pela corrente para espectros
    data = espectros.normalize_spectrum(data, current=100, energy_u='eV', flux_u='ph/s/eV')
    espec[file.split('/')[-1]] = data

    # Carregar dados de um arquivo
    file = 'spectrum_data/Hibisco/HIB_CPMU14_Flux_150urad_Kmax.txt'
    data = espectros.get_spectrum_data(file)
    # Converter dados de largura de banda para energia
    data = espectros.bandwidth_to_energy(data, current=100, energy_u='eV', flux_u='ph/s/0.1%')
    espec[file.split('/')[-1]] = data

    # Plotar dados
    espectros.plot_spectrum_data(espec, title='Sabia x Hibisco')
    # Salvar imagem do plot
    espectros.plot_spectrum_data(espec, title='Sabia x Hibisco', fileout='SabiaHibisco.png')


    # -------------------------------------------------
    # Escrever espectro no formato utilizado pelo Fluka
    # -------------------------------------------------
    espectros = Espectros()

    # Carregar dados de um arquivo
    file = 'spectrum_data/Sussuarana/OPT/SUSSUARANA_SWLS_flux_1p58x0p66mrad2_lowE.txt'
    data = espectros.get_spectrum_data(file)
    # Selecionando as colunas de energia e fluxo
    # Necessário quando o fluxo não é a coluna de índice 1
    data = data[:,[0,3]]
    # Converter dados de largura de banda para energia
    data = espectros.bandwidth_to_energy(data, current=100, energy_u='keV', flux_u='ph/s/0.1%')
    # Escrever dados em um arquivo
    espectros.write_data_file(data, 'SUSSUARANA_SWLS_flux_1p58x0p66mrad2_lowE.spectrum', energy_u='keV', current=100, decimal_places=5)


    # --------------------------------------------
    # Plotar comparativo de espectros em uma pasta
    # --------------------------------------------
    espectros = Espectros()

    # Carregar dados de uma pasta
    folder = 'spectrum_data/Hibisco/HIB_source_flux'
    data = espectros.plot_folder_spectrum(folder, spectrum_type='bandwidth', energy_u='eV', flux_u='ph/s/0.1%', current=100)


    # --------------------------------------------
    # Pegar o fluxo integrado de um espectro
    # --------------------------------------------
    # Carregar dados de um arquivo
    file = 'spectrum_data/Quati/OPT/optica/VS2/flux_Pt_2p25mrad_1p1X0p18mrad2.txt'
    data = espectros.get_spectrum_data(file)
    integrated_spectrum = espectros.integrate_spectrum(data, energy_u='eV', flux_u='ph/s/eV', current=100)
    factor = 3600 * 500 * 1e-6 * 2
    print(f'Espectro integrado: {integrated_spectrum:.4e}')
    print(f'Fator: {integrated_spectrum:.4e}')