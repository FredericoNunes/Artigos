import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

def graficoPreco(ae, nome):
    # Create "Y High" and "Y Low" values as 5% devs from mean
    high, low = np.mean(ae.ygrid) * 1.05, np.mean(ae.ygrid) * .95
    iy_high, iy_low = (np.searchsorted(ae.ygrid, x) for x in (high, low))

    fig, ax = plt.subplots(figsize=(15, 5))
    #ax.set_title(f'{nome}')

    # Extract a suitable plot grid
    x = []
    q_low = []
    q_high = []
    for i in range(ae.nB):
        b = ae.Bgrid[i]
        if -0.5 <= b <= 0:
            x.append(b)
            q_low.append(ae.Q[iy_low, i])
            q_high.append(ae.Q[iy_high, i])
    ax.plot(x, q_high, '-o', label="$y_{Acima}$")
    ax.plot(x, q_low, '-o', label="$y_{Abaixo}$")
    ax.legend(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.axvline(x=-.15, color='green')
    plt.axvline(x=-.1, color='green')
    plt.axvline(x=-.05, color='green')
    limite_de_anotation_1 = 1
    for pos, (i, j) in enumerate(zip(x, q_high)):
        if str("{0:.3f}".format(q_high[pos])) != str("{0:.3f}".format(q_high[pos-1])) and limite_de_anotation_1 <= 7:
            ax.annotate(str("{0:.3f}".format(j)), xy=(i, j + 0.05),size=17)
            limite_de_anotation_1 += 1
    limite_de_anotation = 0
    for pos, (i, j) in enumerate(zip(x, q_low)):
        if str("{0:.3f}".format(q_high[pos])) != str("{0:.3f}".format(q_high[pos - 1])) and limite_de_anotation <= 7:
            ax.annotate(str("{0:.3f}".format(j)), xy=(i, j - 0.06),size=17)
            limite_de_anotation += 1
    #for i, j in zip(x, q_low):
    #    ax.annotate(str(j), xy=(i, j))
    ax.set_xlabel("$B'$",fontsize=20)
    ax.set_ylabel("$Preço Par$",fontsize=20)
    ax.set_xlim(ae.Bgrid.min()-.1, 0.05)
    #ax.legend(loc='upper left', frameon=False)
    #return ({"q_high":q_high,"q_low":q_low}
    #fig.savefig('preco par '+nome, format='pdf')
    plt.subplots_adjust(left=0.04, right=0.98)
    with PdfPages(f'preco_par_{nome}_pdf.pdf') as pdf:
        pdf.savefig(fig)

        # plt.show()


def graficoJuros(ae, nome):
    # Create "Y High" and "Y Low" values as 5% devs from mean
    high, low = np.mean(ae.ygrid) * 1.05, np.mean(ae.ygrid) * .95
    iy_high, iy_low = (np.searchsorted(ae.ygrid, x) for x in (high, low))
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.axvline(x=-.15, color='green')
    plt.axvline(x=-.1, color='green')
    plt.axvline(x=-.05, color='green')
    #ax.set_title(f'{nome}')

    # Extract a suitable plot grid
    x = []
    z = []
    q_low = []
    q_high = []
    for i in range(ae.nB):
        b = ae.Bgrid[i]
        if -0.5 <= b <= 0.01:
            if (1 / ae.Q[iy_high, i] - 1) <= 1:
                q_high.append(1 / ae.Q[iy_high, i] - 1)
                x.append(b)
            if (1 / ae.Q[iy_low, i]) - 1 <= 1:
                z.append(b)
                q_low.append(1 / ae.Q[iy_low, i] - 1)
    ax.set_ylim([-.05, .55])
    ax.plot(x, q_high, '-o', label="$y_{Acima}$")
    ax.plot(z, q_low, '-o', label="$y_{Abaixo}$")

    limite_de_anotation_1 = 1
    for pos, (i, j) in enumerate(zip(x, q_high)):
        if str("{0:.3f}".format(q_high[pos])) != str("{0:.3f}".format(q_high[pos-1])) and limite_de_anotation_1 <= 7:
            ax.annotate(str("{0:.3f}".format(j)) , xy=(i, j - 0.05), size=17)
            limite_de_anotation_1 += 1
    limite_de_anotation = 1
    for pos, (i, j) in enumerate(zip(z, q_low)):
        if str("{0:.3f}".format(q_high[pos])) != str("{0:.3f}".format(q_high[pos - 1])) and limite_de_anotation <= 7:
            ax.annotate(str("{0:.3f}".format(j)) , xy=(i, j + 0.03), size=17)
            limite_de_anotation += 1

    ax.set_xlabel("$B'$",fontsize=20)
    ax.set_ylabel("$Juros$",fontsize=20)
    ax.set_xlim(ae.Bgrid.min() - .05, 0.05)
    ax.legend(loc='upper right', fontsize=20)
    #return ({"q_high":q_high,"q_low":q_low})
    #fig.savefig('Juros ' + nome,format='pdf')
    plt.subplots_adjust(left=0.04, right=0.98)
    with PdfPages(f'juros_{nome}_pdf.pdf') as pdf:
        pdf.savefig(fig)

    # plt.show()


def graficoPoupanca(ae,nome):
    # Create "Y High" and "Y Low" values as 5% devs from mean
    high, low = np.mean(ae.ygrid) * 1.05, np.mean(ae.ygrid) * .95
    iy_high, iy_low = (np.searchsorted(ae.ygrid, x) for x in (high, low))
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.set_title(f'{nome}')

    # Extract a suitable plot grid
    x = []
    z = []
    q_low = []
    q_high = []
    for i in range(ae.nB):
        b = ae.Bgrid[i]
        if -0.25 <= b <= 0.01:
            if (1 / ae.Q[iy_high, i] - 1) <= 1:
                q_high.append(1 / ae.Q[iy_high, i] - 1)
                x.append(b)
            if (1 / ae.Q[iy_low, i]) - 1 <= 1:
                z.append(b)
                q_low.append(1 / ae.Q[iy_low, i] - 1)
    ax.plot(x, x, '-o', label="$y_{Acima}$")
    ax.plot(z, z, '-o', label="$y_{Abaixo}$")
    #for pos, (i, j) in enumerate(zip(ae.Bgrid, x)):
    #    if str("{0:.2f}".format(x[pos])) != str("{0:.2f}".format(x[pos - 1])):
    #        ax.annotate(str("{0:.2f}".format(j)) + "%", xy=(i, j - 0.05))
    #for pos, (i, j) in enumerate(zip(ae.Bgrid, z)):
    #    if str("{0:.2f}".format(q_high[pos])) != str("{0:.2f}".format(z[pos - 1])):
    #        ax.annotate(str("{0:.2f}".format(j)) + "%", xy=(i, j + 0.03))

    ax.set_xlabel("$B$")
    ax.legend(loc='upper right', frameon=False)
    #with PdfPages(f'preco par {nome}_pdf.pdf') as pdf:
    #    pdf.savefig(fig)

    # plt.show()

def graficoFuncaoValor(ae, nome):
    # Create "Y High" and "Y Low" values as 5% devs from mean
    high, low = np.mean(ae.ygrid) * 1.05, np.mean(ae.ygrid) * .95
    iy_high, iy_low = (np.searchsorted(ae.ygrid, x) for x in (high, low))
    fig, ax = plt.subplots(figsize=(20, 8))
    #ax.set_title(f'{nome}')
    ax.plot(ae.Bgrid, ae.V[iy_high], '-o', label="$y_{Acima}$")
    ax.plot(ae.Bgrid, ae.V[iy_low], '-o', label="$y_{Abaixo}$")
    ax.legend(loc='upper left')


    ax.set_xlabel("$B$",fontsize=25)
    ax.set_ylabel("$V(y, B)$",fontsize=25)
    ax.set_xlim(ae.Bgrid.min()-.05, 0.05)
    ax.legend(fontsize=25)
    plt.yticks(fontsize=25)
    plt.xticks(fontsize=27)

    count = 0
    eliminar_primeiro_print = 0
    for pos, (i, j) in enumerate(zip(ae.Bgrid, ae.V[iy_high][2:])):
        if count < 1:
            if str("{0:.7f}".format(ae.V[iy_high][pos])) != str("{0:.7f}".format(ae.V[iy_high][pos - 1])) and eliminar_primeiro_print != 0:
                ax.annotate(str("{0:.2f}".format(i)), xy=(i, j + 0.05),size=25)
                plt.axvline(x=i, color='blue',linewidth=4)
                count += 1
        eliminar_primeiro_print += 1
    count_low = 0
    eliminar_primeiro_print_low = 0
    for pos, (i, j) in enumerate(zip(ae.Bgrid, ae.V[iy_high][2:])):
        if count_low < 1:
            if str("{0:.7f}".format(ae.V[iy_low][pos])) != str("{0:.7f}".format(ae.V[iy_low][pos - 1])) and eliminar_primeiro_print_low != 0:
                ax.annotate(str("{0:.2f}".format(i)), xy=(i, j - 0.98),size=25)
                plt.axvline(x=i, color='orange',linewidth=4)
                count_low += 1
        eliminar_primeiro_print_low += 1
    #return ({"Bgrid":ae.Bgrid,"ae.V":ae.V[iy_high]})
    #fig.savefig('Funcao Valor ' + nome)
    plt.subplots_adjust(left=0.083, right=0.98)
    with PdfPages(f'funcao_valor_{nome}_pdf.pdf') as pdf:
        pdf.savefig(fig)

    # plt.show()


def graficoDefault(ae, nome):
    # Create "Y High" and "Y Low" values as 5% devs from mean
    xx, yy = ae.Bgrid, ae.ygrid

    zz = ae.default_prob
    # Create figure
    fig, ax = plt.subplots(figsize=(15, 5))
    hm = ax.pcolormesh(xx, yy, zz)
    cax = fig.add_axes([.92, .1, .02, .8])
    fig.colorbar(hm, cax=cax)
    ax.axis([-0.30, 0.005, 0.7, 1.4])  # yy.max()
    ax.set(xlabel="$B'$", ylabel="$y$", title=f'{nome}')
    # plt.show()


def simulacao(ae):
    T = 250
    y_vec, B_vec, q_vec, c_vec, default_vec = ae.simulate(T)

    np.random.seed(42)
    c_sim = c_vec
    spread_sim = []
    tb_sim = []

    for i in range(len(B_vec) - 1):
        r = 1 / q_vec[i+1] - 1
        tb = (y_vec[i+1] - c_sim[i]) / y_vec[i]
        spread_sim.append(r * 100)
        tb_sim.append(tb * 100)


    spread_sim.append(r * 100)
    tb_sim.append(tb * 100)



    Parametros = {
        'input': {'variavel': ['β', 'γ', 'r', 'ρ', 'η', 'θ'],
                  'valor': [round(ae.β, 6), round(ae.γ, 6), round(ae.r, 6), round(ae.ρ, 6), round(ae.η, 6),
                            round(ae.θ, 6)]
                  },

        'simulacao_1': {'dados simulados': ['Spread Taxa de Juros', 'Balança Comercial', 'Consumo', 'Produto'],
                        'média(x)': [round(np.mean(spread_sim), 6), round(np.mean(tb_sim), 6), round(np.mean(c_sim), 6),
                                     round(np.mean(y_vec), 6)],
                        'desvio padrão(x)': [round(np.std(spread_sim), 6), round(np.std(tb_sim), 6),
                                             round(np.std(c_sim), 6), round(np.std(y_vec), 6)],
                        'corr(x,y)': [round(np.corrcoef(spread_sim, y_vec)[0][1], 6),
                                      round(np.corrcoef(tb_sim, y_vec)[0][1], 6),
                                      round(np.corrcoef(c_sim, y_vec)[0][1], 6), ''],
                        'corr(x,r-spread)': ['', round(np.corrcoef(spread_sim, tb_sim)[0][1], 6),
                                             round(np.corrcoef(spread_sim, c_sim)[0][1], 6),
                                             round(np.corrcoef(spread_sim, y_vec)[0][1], 6)]},

        'simulacao_2': {'variavel': ['mean dívida externa', 'mean trade balance', 'mean default Probability'],
                        'valor': [round(np.mean(B_vec), 6), round(np.mean(tb_sim), 6), round(np.mean(default_vec), 6)]
                        },
    }

    return Parametros

def plot_simulacao(ae):
    T = 250

    np.random.seed(42)
    y_vec, B_vec, q_vec, c_vec, default_vec = ae.simulate(T)

    # Pick up default start and end dates
    start_end_pairs = []
    i = 0
    while i < len(default_vec):
        if default_vec[i] == 0:
            i += 1
        else:
            # If we get to here we're in default
            start_default = i
            while i < len(default_vec) and default_vec[i] == 1:
                i += 1
            end_default = i - 1
            start_end_pairs.append((start_default, end_default))

    plot_series = (y_vec, B_vec, q_vec)
    titles = 'output', 'foreign assets', 'bond price'

    fig, axes = plt.subplots(len(plot_series), 1, figsize=(10, 12))
    fig.subplots_adjust(hspace=0.3)

    for ax, series, title in zip(axes, plot_series, titles):
        # Determine suitable y limits
        s_max, s_min = max(series), min(series)
        s_range = s_max - s_min
        y_max = s_max + s_range * 0.1
        y_min = s_min - s_range * 0.1
        ax.set_ylim(y_min, y_max)
        for pair in start_end_pairs:
            ax.fill_between(pair, (y_min, y_min), (y_max, y_max),
                            color='k', alpha=0.3)
        ax.grid()
        ax.plot(range(T), series, lw=2, alpha=0.7)
        ax.set(title=title, xlabel="time")

    plt.show()

    return plt.show()