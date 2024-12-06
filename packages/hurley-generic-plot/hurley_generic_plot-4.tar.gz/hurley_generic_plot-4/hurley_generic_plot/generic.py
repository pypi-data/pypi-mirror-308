import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr, pearsonr

def plot_correlation(
    df_toplot, x_value, y_value, 
    groupby=None, group_order=None, group_color=None,
    xlab=None, ylab=None, title = None,
    correlation= None, # 'spearman' or 'pearson'
    height=3.5, aspect=1.2, 
    lab_fontsize = 15, title_fontsize = 15, legend_loc = 'upper center',
    scatter_kws=None
):
    """
    Create a correlation plot with optional grouping and correlation statistics.
    
    Parameters:
    -----------
    df_toplot : pandas DataFrame
        Input dataframe containing the data
    x_value : str
        Column name for x-axis variable
    y_value : str
        Column name for y-axis variable
    groupby : str, optional
        Column name for grouping
    group_order : list, optional
        Order of groups to display
    group_color : dict, optional
        Color mapping for groups
    xlab : str, optional
        X-axis label (defaults to x_value)
    ylab : str, optional
        Y-axis label (defaults to y_value)
    correlation :
        Type of correlation to calculate ('spearman' or 'pearson')
    height : float, default=3.5
        Height of the figure in inches
    aspect : float, default=1.2
        Aspect ratio of the figure
    scatter_kws : dict, optional
        Additional keyword arguments for scatter plot
        
    Returns:
    --------
    matplotlib.axes.Axes
        The plot axes
    """
    # Set default values
    xlab = xlab or x_value
    ylab = ylab or y_value
    scatter_kws = scatter_kws or {
        'edgecolor': 'white',
        'linewidths': 0.8
    }
    
    # Determine groups if not specified
    if groupby:
        if group_order is None:
            group_order = sorted(df_toplot[groupby].unique())
        
        if group_color is None:
            group_color = dict(zip(group_order, sns.color_palette("colorblind", len(group_order))))
    
    # Create title with correlation statistics if requested
    if correlation:
        title = title or ""
        assert correlation in ['spearman','pearson'], "correlation can be only spearman or pearson"
        corr_func = spearmanr if correlation == 'spearman' else pearsonr
        
        if groupby:
            for group in group_order:
                df_sub = df_toplot[df_toplot[groupby] == group][[x_value, y_value]].dropna()
                rho, p_value = corr_func(df_sub[x_value], df_sub[y_value])
                title += f'\n{group}: p = {np.round(p_value,2)}, r = {np.round(rho,2)}'
        else:
            df_sub = df_toplot[[x_value, y_value]].dropna()
            rho, p_value = corr_func(df_sub[x_value], df_sub[y_value])
            title += f'\np = {np.round(p_value,2)}, r = {np.round(rho,2)}'
    
    # Create plot
    g = sns.lmplot(
        data=df_toplot, 
        x=x_value,
        y=y_value, 
        hue=groupby,
        hue_order=group_order,
        palette=group_color,
        height=height,
        aspect=aspect,
        scatter_kws=scatter_kws,
        legend=None
    )
    
    ax = plt.gca()

    # Set labels and title
    ax.set_xlabel(xlab, fontsize=lab_fontsize)
    ax.set_ylabel(ylab, fontsize=lab_fontsize)
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    
    # Add legend if grouping is used
    if groupby:
        ax.legend(title=groupby, loc=legend_loc)
    
    return ax

