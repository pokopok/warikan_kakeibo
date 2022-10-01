import plotly.graph_objects as go

class GraphGenerator:
    """ビューから呼び出されて、グラフをhtmlにして返す"""

    def month_pie(self, labels, values):
        """月間支出の円グラフ"""
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=labels,
                             values=values))

        return fig.to_html(include_plotlyjs=False)

    def month_daily_bar(self, x_list, y_list):
        """月間支出の日別棒グラフ"""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
        ))

        return fig.to_html(include_plotlyjs=False)