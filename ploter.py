from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import base64
from io import BytesIO

def plot_dates(dates):

    plt.style.use("seaborn-whitegrid")

    days = dates.keys()
    nr_events = dates.values()

    fig = Figure()
    ax = fig.subplots()
    ax.plot(days, nr_events, 'o-') 

    ax.set_ylim(ymin=0) 
    ax.set_ylabel("Nr of events") # Label y axis
    ax.set_title("Event counts per day")  # plot title

    date_format = mpl_dates.DateFormatter("%b %d")
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

