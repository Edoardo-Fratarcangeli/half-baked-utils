from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PieChartCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 4))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)

    def plot_languages(self, df, username):
        self.ax.clear()
        if df is not None and not df.empty:
            self.ax.pie(
                df["percentage"],
                labels=df["language"],
                autopct="%1.1f%%",
                startangle=140
            )
            self.ax.set_title(f"Linguaggi GitHub – {username}")
        else:
             self.ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.draw()

    def save_png(self, path):
        self.fig.savefig(path, dpi=200, bbox_inches="tight")
