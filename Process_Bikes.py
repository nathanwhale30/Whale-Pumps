import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter
import glob

def process_bikes(user, start_date):
    print(user + "'s Bikes Function Running")
    if start_date is None or start_date == "":
        return