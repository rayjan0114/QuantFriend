import matplotlib.pyplot as plt
plt.style.use('ggplot')


def visuialize_performance(back_testor, *data):
    ylabel_dict = {
               'fontsize'            : 12,
               'horizontalalignment' : 'right',
               'rotation'            : 'horizontal',}
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan=7, colspan=1)
    ax2 = plt.subplot2grid((10,1), (7,0), rowspan=10, colspan=1,sharex=ax1)   
    for data_i in data:
        ax1.plot(data_i.index, data_i, label=data_i.columns[0])
    ax1.legend(loc='upper right')
    ax1.set_ylabel('price', **ylabel_dict)
    account = back_testor.get_account()[:back_testor.count]
    ax2.plot(account, color='gray')
    ax2.set_ylabel('account', **ylabel_dict)
    for stockID, signal in back_testor.get_signals().items():
        ax2.scatter(signal[signal[stockID] > 0].index, account.loc[
            signal[signal[stockID] > 0].index, 'account'].values, color='red', s=25, marker="^", zorder=3)
        ax2.scatter(signal[signal[stockID] < 0].index, account.loc[
            signal[signal[stockID] < 0].index, 'account'].values, color='green', s=25, marker="v", zorder=3)
     
    plt.tight_layout()
    do_save=True
    if do_save:
        plt.savefig('rst.jpg', quality=100)

# visuialize_performance(back_testor, df[['13MA']], df[['34MA']], trading_data[['2380_close']])
