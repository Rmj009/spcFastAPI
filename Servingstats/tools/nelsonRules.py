import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# df = pd.read_csv('workbook_name.csv', sep=',',header=0); nmp = df.to_numpy() ;data = nmp[:,11]#; data = pd.DataFrame(nmp[:,11])
# data = spcTable.data
"""
REFERENCE:
Douglas C. Montgomery-Introduction to statistical quality control 7th edtition-Wiley (2009)
Part III chapter 5.3, p205.
"""

def _sliding_chunker(original, segment_len, slide_len):
    """Split a list into a series of sub-lists...

    each sub-list window_len long,
    sliding along by slide_len each time. If the list doesn't have enough
    elements for the final sub-list to be window_len long, the remaining data
    will be dropped.

    e.g. sliding_chunker(range(6), window_len=3, slide_len=2)
    gives [ [0, 1, 2], [2, 3, 4] ]
    """
    chunks = []
    for pos in range(0, len(original), slide_len):
        chunk = np.copy(original[pos:pos + segment_len])
        if len(chunk) != segment_len:
            continue
        chunks.append(chunk)
    return chunks


def _clean_chunks(original, modified, segment_len):
    """appends the output argument to fill in the gaps from incomplete chunks"""
    results = []
    results = modified
    for i in range(len(original) - len(modified)):
        results.append(0)

    # set every value in a qualified chunk to 1
    for i in reversed(range(len(results))):
        if results[i] == 1:
            for d in range(segment_len):
                results[i+d] = 1
    return results

def plot_rules(data, chart_type=2):
    data = pd.DataFrame(data)

    if chart_type == 1:
        columns = data.columns[1:]
        fig, axs = plt.subplots(1, 1, figsize=(20, 20))
        fig.subplots_adjust(hspace=1, wspace=.5)

        axs = axs.ravel()
        for i in range(len(columns)):
           axs[i].plot(data.iloc[:, 0])
           axs[i].plot(data.iloc[:, 0][(data.iloc[:, i+1] == 1)], 'x')
           axs[i].set_title(columns[i])

        return fig

    elif chart_type == 2:
        # plot_num = len(data.columns[1:])
        fig = plt.figure(figsize=(20, 10))
        axs = fig.add_subplot(111)
        
        axs.plot(data.iloc[:, 0])

        marker = ['H', '+', '.', 'o', '*', '<', '>', '^']
        columns = data.columns[1:]

        for i in range(len(data.columns[1:])):
            axs.plot(data.iloc[:, 0][(data.iloc[:, i+1] == 1)], ls='', marker=marker[i], markersize=20, label=columns[i])

        plt.legend()
        # plt.show()
        plt.savefig('static/img/Nelson.png')

        return fig

# plot_rules(data=data)

def apply_rules(original, rules='all', chart_type=2):
    
    data_mean = np.mean(original)
    data_sig = np.std(original)
    if rules == 'all':
        rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
    df = pd.DataFrame(original)
    for i in range(len(rules)):
        df[rules[i].__name__] = rules[i](original= original, mean = data_mean, sigma = data_sig)
    # fig = plot_rules(df, chart_type)

    return df #, fig


def rule1(original, mean, sigma):
    """One point is more than 3 standard deviations from the mean."""
    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    copy_original = original
    ulim = mean + (sigma * 3)
    llim = mean - (sigma * 3)

    results = []
    for i in range(len(copy_original)):
        if copy_original[i] < llim:
            results.append(1)
        elif copy_original[i] > ulim:
            results.append(1)
        else:
            results.append(0)

    return results


def rule2(original, mean, sigma):
    """Nine (or more) points in a row are on the same side of the mean."""
    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    copy_original = original
    segment_len = 9

    side_of_mean = []
    for i in range(len(copy_original)):
        if copy_original[i] > mean:
            side_of_mean.append(1)
        else:
            side_of_mean.append(-1)

    chunks = _sliding_chunker(side_of_mean, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        if chunks[i].sum() == segment_len or chunks[i].sum() == (-1 * segment_len):
            results.append(1)
        else:
            results.append(0)

    # clean up results
    results = _clean_chunks(copy_original, results, segment_len)

    return results

def rule3(original, mean, sigma):
    """Six (or more) points in a row are continually increasing (or decreasing)."""
    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 6
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        chunk = []

        # Test the direction with the first two data points and then iterate from there.
        if chunks[i][0] < chunks[i][1]: # Increasing direction
            for d in range(len(chunks[i])-1):
                if chunks[i][d] < chunks[i][d+1]:
                    chunk.append(1)
        else: # decreasing direction
            for d in range(len(chunks[i])-1):
                if chunks[i][d] > chunks[i][d+1]:
                    chunk.append(1)

        if sum(chunk) == segment_len-1:
            results.append(1)
        else:
            results.append(0)

    # clean up results
    results = _clean_chunks(copy_original, results, segment_len)

    return results

def rule4(original, mean, sigma):
    """Fourteen (or more) points in a row alternate in direction, increasing then decreasing."""
    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 14
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        current_state = 0
        for d in range(len(chunks[i])-1):
            # direction = int()
            if chunks[i][d] < chunks[i][d+1]:
                direction = -1
            else:
                direction = 1

            if current_state != direction:
                current_state = direction
                result = 1
            else:
                result = 0
                break

        results.append(result)

    # fill incomplete chunks with 0
    results = _clean_chunks(copy_original, results, segment_len)

    return results

def rule5(original, mean, sigma):
    """Two (or three) out of three points in a row are more than 2 standard deviations from the mean in the same
    direction."""

    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 2
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        if all(i > (mean + sigma * 2) for i in chunks[i]) or all(i < (mean - sigma * 2) for i in chunks[i]):
            results.append(1)
        else:
            results.append(0)

    # fill incomplete chunks with 0
    results = _clean_chunks(copy_original, results, segment_len)

    return results

def rule6(original, mean, sigma):
    """Four (or five) out of five points in a row are more than 1 standard deviation from the mean in the same
    direction."""

    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 4
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        if all(i > (mean + sigma) for i in chunks[i]) or all(i < (mean - sigma) for i in chunks[i]):
            results.append(1)
        else:
            results.append(0)

    # fill incomplete chunks with 0
    results = _clean_chunks(copy_original, results, segment_len)

    return results

def rule7(original, mean, sigma): #temporary off
    """Fifteen points in a row are all within 1 standard deviation of the mean on either side of the mean."""

    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 15
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len = 15, slide_len = 1)

    results = []
    for i in range(len(chunks)):
        if all((mean - sigma) < i < (mean + sigma) for i in chunks[i]) :
            results.append(1) # 1
        else:
            results.append(0)

    # fill incomplete chunks with 0
    results = _clean_chunks(original = copy_original, modified= results, segment_len = segment_len)
    # print(results)

    return results

def rule8(original, mean, sigma):

    """Eight points in a row exist, but none within 1 standard deviation of the mean, and the points are in both
    directions from the mean."""

    if mean is None:
        mean = original.mean()

    if sigma is None:
        sigma = original.std()

    segment_len = 8
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)

    results = []
    for i in range(len(chunks)):
        if all(i < (mean - sigma) or i > (mean + sigma) for i in chunks[i])\
                and any(i < (mean - sigma) for i in chunks[i])\
                and any(i > (mean + sigma) for i in chunks[i]):
            results.append(1)
        else:
            results.append(0)

    # fill incomplete chunks with 0
    results = _clean_chunks(copy_original, results, segment_len)

    return results



def drawchart2(original):
    """Plot RawData"""
    text_offset = 70
    mean = np.mean(original)
    sigma = np.std(original)
    # print("###",[mean,sigma])
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(original, color='blue', linewidth=1.5)

    # plot mean
    ax1.axhline(mean, color='r', linestyle='--', alpha=0.5)
    ax1.annotate('$\overline{x}$', xy=(len(original), mean), textcoords=('offset points'),xytext=(text_offset, 0), fontsize=18)

    # plot 1-3 standard deviations
    sigma_range = np.arange(1,4)
    for i in range(len(sigma_range)):
        ax1.axhline(mean + (sigma_range[i] * sigma), color='black', linestyle='-', alpha=(i+1)/10)
        ax1.axhline(mean - (sigma_range[i] * sigma), color='black', linestyle='-', alpha=(i+1)/10)
        ax1.annotate('%s $\sigma$' % sigma_range[i], xy=(len(original), mean + (sigma_range[i] * sigma)),
                    textcoords=('offset points'),
                    xytext=(text_offset, 0), fontsize=18)
        ax1.annotate('-%s $\sigma$' % sigma_range[i],
                    xy=(len(original), mean - (sigma_range[i] * sigma)),
                    textcoords=('offset points'),
                    xytext=(text_offset, 0), fontsize=18)
    # plt.show()
    plt.savefig('static/img/classicialcc2.png')
    return fig 

# result = apply_rules(original=data)
# # print('rrrr',enumerate(result))
# # sns.set_style('whitegrid')
# # sns.kdeplot([j for i,j in enumerate(result[0])], bw=0.5)
# result[0].plot(kind='density')
# plt.show()

# drawchart2(original=result[0])
# plt.show()
# print('result',result.head(), sep='/n')