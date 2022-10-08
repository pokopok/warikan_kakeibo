import plotly.graph_objects as go

class GraphGenerator:
    """ビューから呼び出されて、グラフをhtmlにして返す"""
    pie_line_color = '#000'
    plot_bg_color = 'rgb(255,255,255)'
    paper_bg_color = 'rgb(255,255,255)'
    month_bar_color = 'indianred'
    font_color = 'dimgray'
    expenses_color = 'tomato'

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

    def transition_plot(self,
                        x_list_expenses=None,
                        y_list_expenses=None):
        """推移ページの複合グラフ"""
        fig = go.Figure()
        
        if x_list_expenses and y_list_expenses:
            fig.add_trace(go.Bar(
                x=x_list_expenses,
                y=y_list_expenses,
                name='expenses',
                opacity=0.5,
                marker_color=self.expenses_color
            ))

        fig.update_layout(
            paper_bgcolor=self.paper_bg_color,
            plot_bgcolor=self.plot_bg_color,
            font=dict(size=14, color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0, r=0, b=20, t=30, ),
            yaxis=dict(
                showgrid=False,
                linewidth=1,
                rangemode='tozero'))
        # fig.update_yaxes(visible=False, fixedrange=True)
        # fig.update_yaxes(automargin=True)
        return fig.to_html(include_plotlyjs=False)