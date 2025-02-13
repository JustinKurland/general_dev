import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import numpy as np

def apply_gs_theme(palette='default'):
    """
    Applies the Goldman Sachs theme to all Matplotlib plots and ensures 
    that all plot types (bar, line, scatter, hist, boxplot) automatically use theme colors.

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

    divergent_colors = ['#EB6B63', '#56A940']
    divergent_contrast_colors = ['#E0731A', '#3B7CDE']

    # Choose the appropriate color palette
    selected_colors = (
        divergent_colors if palette == 'divergent' else 
        divergent_contrast_colors if palette == 'divergent_contrast' else 
        categorical_colors
    )

    gs_theme = {
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
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'axes.unicode_minus': False,
        
        'axes.prop_cycle': cycler('color', selected_colors),
        'axes.autolimit_mode': 'data',
        'axes.xmargin': 0.05,
        'axes.ymargin': 0.05,

        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.8,
        'grid.color': '#DDDDDD',

        'legend.loc': 'best',
        'legend.frameon': True,
        'legend.fontsize': 14,
        'legend.title_fontsize': 16,

        'figure.dpi': 300
    }

    matplotlib.rcParams.update(gs_theme)

    # Auto-apply colors to all plot types
    def auto_color_wrapper(original_func):
        """ Wraps Matplotlib plotting functions to apply theme colors automatically. """
        def wrapper(*args, **kwargs):
            if 'color' not in kwargs or kwargs['color'] is None:
                colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
                kwargs['color'] = colors[:len(args[0])] if isinstance(args[0], (list, np.ndarray)) else colors[0]
            return original_func(*args, **kwargs)
        return wrapper

    # Apply automatic color handling to key plot functions
    plt.bar = auto_color_wrapper(plt.bar)
    plt.plot = auto_color_wrapper(plt.plot)
    plt.scatter = auto_color_wrapper(plt.scatter)
    plt.hist = auto_color_wrapper(plt.hist)

# Apply the theme
apply_gs_theme()


# ---- TEST PLOTS ----

# Example Bar Chart
categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
values = [25, 40, 15, 30, 20, 35, 10, 45]

plt.figure(figsize=(10, 6))
plt.bar(categories, values)  # Now automatically colored
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Bar Chart with Auto Theme Colors")
plt.grid(axis='y', linestyle='--')
plt.show()


# Example Line Plot
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y1, label="sin(x)")
plt.plot(x, y2, label="cos(x)")
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.title("Line Plot with Auto Theme Colors")
plt.legend()
plt.show()


# Example Scatter Plot
x = np.random.rand(50)
y = np.random.rand(50)

plt.figure(figsize=(10, 6))
plt.scatter(x, y)
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.title("Scatter Plot with Auto Theme Colors")
plt.show()


# Example Histogram
data = np.random.randn(1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, edgecolor='black')
plt.xlabel("Bins")
plt.ylabel("Frequency")
plt.title("Histogram with Auto Theme Colors")
plt.show()
