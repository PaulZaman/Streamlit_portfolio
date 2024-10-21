import plotly.express as px

def histogram_with_stats(data, column, title):
    # Calculate quartiles and mean
    quartiles = data[column].quantile([0.25, 0.5, 0.75])
    mean = data[column].mean()

    # Create the histogram
    fig = px.histogram(data, x=column, nbins=50, title=title)

    # Add quartiles and mean lines
    fig.add_shape(type="line", x0=quartiles[0.25], x1=quartiles[0.25], y0=0, y1=1, 
                  line=dict(color="green", dash="dash"), xref='x', yref='paper')
    fig.add_shape(type="line", x0=quartiles[0.5], x1=quartiles[0.5], y0=0, y1=1, 
                  line=dict(color="blue", dash="dash"), xref='x', yref='paper')
    fig.add_shape(type="line", x0=quartiles[0.75], x1=quartiles[0.75], y0=0, y1=1, 
                  line=dict(color="green", dash="dash"), xref='x', yref='paper')
    fig.add_shape(type="line", x0=mean, x1=mean, y0=0, y1=1, 
                  line=dict(color="red", dash="solid"), xref='x', yref='paper')
    return fig
