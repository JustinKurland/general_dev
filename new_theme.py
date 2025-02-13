import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler

def apply_gs_theme(palette='default'):
    """
    Applies the Goldman Sachs theme to all Matplotlib plots.
    
    Parameters:
    - palette: str, optional (default='default')
      - 'default': Uses the standard categorical color palette.
      - 'divergent': Uses a red-green color scheme for positive/negative values.
      - 'divergent_contrast': Uses an orange-blue color scheme for accessibility.
    """
    
    # Define Color Palettes
    categorical_colors = [
        '#3B7CDE', '#7297C5', '#A6428C', '#159788', '#E88D43', '#9157C4',
        '#C44545', '#F3C43F', '#B2570D', '#617A27', '#64D1C6', '#7BA9ED',
        '#EDAFDC', '#C7A0E8', '#538CE0', '#E8AD09', '#E07575', '#C761AC',
        '#BFD986', '#E3D0F2'
    ]

    divergent_colors = [
        '#EB6B63',  # functionalRed050 (negative)
        '#56A940'   # functionalGreen050 (positive)
    ]

    divergent_contrast_colors = [
        '#E0731A',  # orange050 (negative)
        '#3B7CDE'   # blue050 (positive)
    ]

    # Choose the appropriate color palette
    if palette == 'divergent':
        selected_colors = divergent_colors
    elif palette == 'divergent_contrast':
        selected_colors = divergent_contrast_colors
    else:
        selected_colors = categorical_colors

    gs_theme = {
        # Axes
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 0.8,
        'axes.grid': True,
        'axes.grid.axis': 'both',
        'axes.grid.which': 'major',
        'axes.titlesize': 18,
        'axes.titleweight': 'normal',
        'axes.titlepad': 6.0,
        'axes.labelsize': 14,
        'axes.labelpad': 4.0,
        'axes.labelweight': 'normal',
        'axes.labelcolor': 'black',
        'axes.axisbelow': 'line',
        'axes.formatter.limits': [-7, 7],
        'axes.formatter.use_locale': False,
        'axes.formatter.use_mathtext': False,
        'axes.formatter.min_exponent': 0,
        'axes.formatter.useoffset': True,
        'axes.formatter.offset_threshold': 4,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'axes.unicode_minus': False,
        
        # Dynamically applied color cycle
        'axes.prop_cycle': cycler('color', selected_colors),

        'axes.autolimit_mode': 'data',
        'axes.xmargin': 0.05,
        'axes.ymargin': 0.05,
        'polaraxes.grid': True,
        'axes3d.grid': True,
        
        # Grid
        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.8,
        'grid.color': '#DDDDDD',

        # Legend
        'legend.loc': 'best',
        'legend.frameon': True,
        'legend.framealpha': 0.8,
        'legend.facecolor': 'inherit',
        'legend.edgecolor': 'inherit',
        'legend.fancybox': True,
        'legend.shadow': False,
        'legend.numpoints': 1,
        'legend.scatterpoints': 1,
        'legend.markerscale': 1.0,
        'legend.fontsize': 14,
        'legend.title_fontsize': 16,
        'legend.borderpad': 0.4,
        'legend.labelspacing': 0.5,
        'legend.handlelength': 2.0,
        'legend.handleheight': 0.7,
        'legend.handletextpad': 0.8,
        'legend.borderaxespad': 0.5,
        'legend.columnspacing': 2.0,

        # Figure Settings
        'figure.dpi': 300
    }

    # Apply the theme to Matplotlib
    matplotlib.rcParams.update(gs_theme)

# Example Usage:
# Apply the default categorical theme
apply_gs_theme()

# Apply the divergent theme for highlighting positive/negative values
# apply_gs_theme(palette='divergent')

# Apply the divergent contrast theme for accessibility
# apply_gs_theme(palette='divergent_contrast')


# Example Plot to Test the Theme
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")

plt.title("Example Plot with Dynamic GS Theme")
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.legend()
plt.show()
