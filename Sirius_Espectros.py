import numpy as np
from matplotlib import pyplot as plt
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
        Carrega dados de espectro de um arquivo.

        Args:
            filename (str): Caminho para o arquivo de espectro.

        Returns:
            numpy.ndarray: Dados do espectro como um array numpy, onde a primeira coluna é a energia e a segunda é o fluxo.
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
        spectrum_lines = []
        for line in lines:
            if '#' in line: continue
            spectrum_lines.append([float(l) for l in line.split()])
        return np.array(spectrum_lines)
    
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

    def plot_folder_spectrum(self, folder, spectrum_type='bandwidth', energy_u='eV', flux_u='ph/s/0.1%', current=1):
        """
        Carrega e plota dados de espectro de vários arquivos em uma pasta.

        Args:
            filename (str): Caminho para a pasta contendo os arquivos de espectro.
            spectrum_type (str, optional): Tipo de espectro nos arquivos. Pode ser 'bandwidth' ou 'energy'. O padrão é 'bandwidth'.
            energy_u (str, optional): Unidade de energia para a conversão/normalização. O padrão é 'eV'.
            flux_u (str, optional): Unidade de fluxo para a conversão/normalização. O padrão é 'ph/s/0.1%'.
            current (float, optional): Corrente da linha de luz. O padrão é 1.
        """
        if not os.path.isdir(folder):
            return
        
        espec = {}
        for file in sorted( os.listdir(folder) ):
            filepath = os.path.join(folder, file)
            data = self.get_spectrum_data(filepath)
            if spectrum_type == 'bandwidth':
                data = self.bandwidth_to_energy(data, energy_u=energy_u, flux_u=flux_u, current=current)
            else:
                data = self.normalize_spectrum(data, energy_u=energy_u, flux_u=flux_u, current=current)
            # print(sum(data[:,1]))
            espec[file] = data
        self.plot_spectrum_data(espec, title=folder)

    def write_data_file(self, data, filename):
        """
        Escreve os dados do espectro em um arquivo.

        Args:
            data (numpy.ndarray): Dados do espectro como um array numpy, onde a primeira coluna é a energia e a segunda é o fluxo.
            filename (str): Nome do arquivo para salvar os dados.
        """
        max1 = max( max( [len(f'{d[0]}') for d in data] ), 12 )
        max2 = max( max( [len(f'{d[1]}') for d in data] ), 14 )
        data_write = [f'{d[0]:>{max1}} {d[1]:>{max2}}\n' for d in data]
        with open(filename, 'w') as f:
            f.write(f'{"#Energy (ev)":>{max1}} {"Flux (ph/s/mA)":>{max2}}\n')
            f.writelines(data_write)
    


        

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
    file = 'spectrum_data/Mogno/OPT/BC_spectrum_043x043_100mA.dat'
    data = espectros.get_spectrum_data(file)
    # Converter dados de largura de banda para energia
    data = espectros.bandwidth_to_energy(data, current=100, energy_u='eV', flux_u='ph/s/0.1%')
    # Escrever dados em um arquivo
    espectros.write_data_file(data, 'mogno.spectrum')


    # --------------------------------------------
    # Plotar comparativo de espectros em uma pasta
    # --------------------------------------------
    espectros = Espectros()
    espec = {}

    # Carregar dados de uma pasta
    folder = 'spectrum_data/Hibisco/HIB_source_flux/CPMU14'
    data = espectros.plot_folder_spectrum(folder, spectrum_type='bandwidth', energy_u='eV', flux_u='ph/s/0.1%', current=100)
