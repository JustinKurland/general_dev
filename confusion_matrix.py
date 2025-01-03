# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pandas_flavor as pf
import warnings
warnings.filterwarnings("ignore")

@pf.register_dataframe_method
def plot_cm(y_true, 
            y_pred, 
            labels, 
            scale_type    = "count",
            lower_color   = "White",
            upper_color   = "#0E4978",
            line_width    = 1,
            line_color    = 'White',
            font_size     = 12,
            ticks         = False,
            cbar          = True,
            title         = "",
            title_weight  = "bold",
            title_size    = "18",
            x_ax_title    = "Predicted",
            y_ax_title    = "Actual",
            x_ax_weight   = "bold",
            y_ax_weight   = "bold",
            ax_title_size = "12",
            figsize       = (6,6)):
    """
    Generate Confusion Matrix with both raw counts and normalized percentages.
    
    Args: 
      y_true ([list]): List of the actual class labels of y
      y_pred ([list]): List of predicted class labels of y
      labels ([list]): List of strings, that are the name and order of class labels in the confusion matrix.
      scale_type ([str, optional]): String of either "count" or "percentage" for scaling confusion matrix color.
      lower_color ([str, optional]): String specifying the color of the lower value of the color scale. Defaults to white.
      upper_color ([str, optional]): String specifying the color of the upper value of the color scale. Defaults to Northwestern Mutual's blue.
      line_width ([float, optional)]: Width of the lines that will divide each cell. Defaults to 1.
      line_color ([str, optional)]: String specifying the color of the lines that will divide each cell. Defaults to white.
      font_size ([float, optional]): Float specifying the size of the font for the count and percentages.
      ticks ([bool, optional]): Boolean specifying whether to include tick marks for class labels. Defaults to false.
      cbar ([bool, optional]): Boolean specifying whether to include the color bar. Defaults to true. 
      title ([str, optional]): String of a title. Default is set for no title.
      title_weight ([str, optional]): String specifying the title weight if title is desired, choices include the default, which is 'bold', 
      'light', 'normal', 'medium', 'semibold', 'heavy', and 'black'.
      title_size ([str, optional]): String of title font size. Default value is 18, adjust only if title is desired.
      x_ax_title ([str, optional]): String of a x-axis title. Default is set to Predicted.  
      y_ax_title  ([str, optional]): String of a y-axis title. Default is set for Actual. 
      x_ax_weight ([str, optional]): String specifying the x-axis title weight if title is desired, choices include the default, which is 'bold', 
      'light', 'normal', 'medium', 'semibold', 'heavy', and 'black'. 
      y_ax_weight ([str, optional]): String specifying the y-axis title weight if title is desired, choices include the default, which is 'bold', 
      'light', 'normal', 'medium', 'semibold', 'heavy', and 'black'.
      ax_title_size ([str, optional]): String of axes title font size. Default value is 12.
      figsize ([int,int]): Size of the figure to be plotted. Defaults to 6X6.
      
    Returns:
       [matplotlib.axes._subplots.AxesSubplot]: A confusion matrix.
       
    Example Binary Classification:
    
        >>> import plot_confusion_matrix
        >>> import numpy as np
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns
        >>> from sklearn.metrics import confusion_matrix
        >>> y_true = [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0 ]
        >>> y_pred = [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1 ]
        >>> labels = [0, 1]
        >>> plot_cm(y_true, y_pred, labels, scale_type="count", font_size=12, title="Confusion Matrix", cbar=False, ticks=True)
        
    Example Multi-Class Classification:
    
        >>> import plot_confusion_matrix
        >>> import numpy as np
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns
        >>> from sklearn.metrics import confusion_matrix
        >>> y_true = ["dog", "cat", "hamster", "cat", "dog", "hamster", "hamster", "dog", "cat", "dog", "hamster", "hamster", "hamster", "hamster", "hamster", "hamster", "hamster", "cat", "dog", "hamster" ]
        >>> y_pred = ["dog", "cat", "hamster", "cat", "hamster", "cat", "hamster", "cat", "dog", "cat", "hamster", "hamster", "hamster", "dog", "cat", "hamster", "hamster", "hamster", "hamster", "dog" ]
        >>> labels = ["dog", "cat", "hamster"]
        >>> plot_cm(y_true, y_pred, labels, scale_type="percentage", font_size=16, title="Animal Classification", cbar=True, ticks=False)  
    """
    
    # Create a confusion matrix, extract the values, calculate normalized percentages
    cm            = confusion_matrix(y_true, y_pred, labels=labels)
    cm_count      = np.sum(cm, axis=1, keepdims=True)
    cm_percentage = cm / cm_count.astype(float) * 100
    annot         = np.empty_like(cm).astype(str)
    nrows, ncols  = cm.shape
    
    # Iterate
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_percentage[i, j]
            if i == j:
                s = cm_count[i]
                annot[i, j] = '%.2f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.2f%%\n%d' % (p, c)
                
    # Northwestern Colors 
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("", [lower_color,upper_color]) 
    
    if scale_type=="count":
    
        # DataFrame Object for Seaborn Heatmap
        cm              = pd.DataFrame(cm, index=labels, columns=labels)
        cm.index.name   = str(y_ax_title)
        cm.columns.name = str(x_ax_title)
        

        # Plot Confusion Matrix
        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yticklabels(labels=ax.get_yticklabels(), va='center')
        ax.set_xticklabels(labels=ax.get_xticklabels(), ha='center')
        ax.tick_params(bottom=ticks, left=ticks)
        plt.rc('font', size=font_size)
        plt.title(str(title), weight=str(title_weight)).set_fontsize(str(title_size))
        plt.xlabel(str(x_ax_title), fontweight=str(x_ax_weight), fontsize=str(ax_title_size))
        plt.ylabel(str(y_ax_title), fontweight=str(y_ax_weight), fontsize=str(ax_title_size))
        sns.heatmap(cm, annot=annot, cmap=cmap, linewidth=line_width, linecolor=line_color, cbar=cbar, fmt='', ax=ax)
        return 
    
    if scale_type=="percentage":
        
        # DataFrame Object for Seaborn Heatmap
        cm              = pd.DataFrame(cm_percentage, index=labels, columns=labels)
        cm.index.name   = str(y_ax_title)
        cm.columns.name = str(x_ax_title)

        # Plot Confusion Matrix
        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yticklabels(labels=ax.get_yticklabels(), va='center')
        ax.tick_params(bottom=ticks, left=ticks)
        plt.rc('font', size=font_size)
        plt.title(str(title), weight=str(title_weight)).set_fontsize(str(title_size))
        plt.xlabel(str(x_ax_title), fontweight=str(x_ax_weight), fontsize=str(ax_title_size))
        plt.ylabel(str(y_ax_title), fontweight=str(y_ax_weight), fontsize=str(ax_title_size))
        sns.heatmap(cm, annot=annot, cmap=cmap, linewidth=line_width, linecolor=line_color, cbar=cbar, fmt='', ax=ax)
        
        return 
