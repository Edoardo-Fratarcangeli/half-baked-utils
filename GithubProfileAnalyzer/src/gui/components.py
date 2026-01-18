from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AnalysisChartCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 4))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        # Adjust bottom to make room for "Others" text
        self.fig.subplots_adjust(bottom=0.25)

    def plot_languages(self, df, username, threshold=5):
        self.ax.clear()
        if df is not None and not df.empty:
            # Filter logic
            main_mask = df["percentage"] >= threshold
            main_df = df[main_mask].copy()
            others_df = df[~main_mask].copy()

            # Prepare plot data
            plot_df = main_df
            
            others_sum = 0
            others_text = ""

            if not others_df.empty:
                others_sum = others_df["percentage"].sum()
                others_bytes = others_df["bytes"].sum()
                # Create a row for "Others"
                others_row = pd.DataFrame([{
                    "language": "Others",
                    "bytes": others_bytes,
                    "percentage": others_sum
                }])
                plot_df = pd.concat([main_df, others_row], ignore_index=True)
                
                # Prepare text for others
                others_list = others_df["language"].tolist()
                others_text = "Others: " + ", ".join(others_list)

            # Sort descending for better bar chart look (if not already)
            # plot_df = plot_df.sort_values(by="percentage", ascending=False) 
            # (Assuming incoming df is already sorted, but appending Others at end is standard)

            # Bar Chart
            bars = self.ax.bar(
                plot_df["language"], 
                plot_df["percentage"],
                color='skyblue',
                edgecolor='navy'
            )

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                self.ax.text(
                    bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom'
                )

            self.ax.set_title(f"GitHub Languages – {username}")
            self.ax.set_ylabel("Percentage")
            self.ax.tick_params(axis='x', rotation=45)

            # Add "Others" text description at the bottom
            if others_text:
                self.fig.text(
                    0.5, 0.02, 
                    others_text, 
                    ha='center', va='bottom', 
                    fontsize=8, color='gray', 
                    wrap=True
                )

        else:
             self.ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        
        self.draw()

    def save_png(self, path):
        self.fig.savefig(path, dpi=200, bbox_inches="tight")

