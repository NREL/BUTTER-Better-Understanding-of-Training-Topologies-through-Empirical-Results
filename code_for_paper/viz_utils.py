import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('image', cmap='viridis')
plt.ion()
normal_font = {'family' : 'DejaVu Sans',
        'weight' : 'medium',
        'size'   : 6}
stats_font = {'family' : 'DejaVu Sans',
        'weight' : 'medium',
        'size'   : 6}
plt.rc('font', **normal_font)

def do_viz(viz_data, dimensions, variable,
           log_x=False, log_y=False, log_z=True, contour_levels=14, title=None,
           plot_data_points=True, x_label=True, y_label=True,
           spines=['left','bottom'],xlim=None,ylim=None,cmap="viridis",
           vmin=None, vmax=None,
           xticks=None, yticks=None,
           plot_landmarks=False,
           landmarks=None):
    X, Y = None, None
    filters = ""
    for key, value in dimensions.items():
        if value == "**X**":
            X = key
        elif value == "**Y**":
            Y = key
        else:
            if type(value) is str:
                value = f"'{value}'"
            filters += (f" `{key}`=={value} &")
    filters = filters[:-1]

    viz_df = viz_data.query(filters)[[X,Y,variable]]
    
    z = viz_df[variable]
    if log_z:
        z = -np.log1p(z)
        
    if viz_df[[X,Y]].duplicated().any():
        print("WARNING: Query contains duplicate rows for chosen indices")

    if plot_data_points != False:
        plt.plot(viz_df[X].to_numpy().flatten(), viz_df[Y].to_numpy().flatten(), '.', markersize=1, alpha=0.1, color='grey')

    plt.tricontourf(viz_df[X], viz_df[Y], z, levels=contour_levels, cmap=cmap, vmin=vmin, vmax=vmax)

    if plot_landmarks:
        if plot_landmarks == "maximum":
            idx = np.argmax(z)
        if plot_landmarks == "minimum":
            idx = np.argmax(z)
        if plot_landmarks != "from_list":
            ix, iy = viz_df[X].values[idx], viz_df[Y].values[idx]
            landmarks.append((ix,iy))
        if plot_landmarks == "from_list":
            ix, iy = landmarks.pop(0)
        plt.plot(ix, iy,
            "^",
            markersize=5,
            alpha=1.0,
            markerfacecolor='black',
            markeredgewidth=1,
            markeredgecolor="white")

    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim(ylim)

    if x_label != False:
        plt.xlabel(X)
        
    if y_label != False:
        plt.ylabel(Y)

    if log_y:
        plt.gca().set_yscale('log')
    if log_x:
        plt.gca().set_xscale('log')

    plt.gca().yaxis.set_ticks_position('none')
    plt.gca().xaxis.set_ticks_position('none')

    if xticks:
        plt.gca().xaxis.set_ticks(xticks)

    if yticks:
        plt.gca().yaxis.set_ticks(yticks)

    if 'left' in spines:
        plt.gca().yaxis.set_ticks_position('left')
        plt.yticks(rotation=90, verticalalignment="center")
    elif 'right' in spines:
        plt.gca().yaxis.set_ticks_position('right')
        plt.yticks(rotation=90, verticalalignment="center")
    else:
        plt.gca().yaxis.set_ticks([])

    if 'bottom' in spines:
        plt.gca().xaxis.set_ticks_position('bottom')
    elif 'top' in spines:
        plt.gca().xaxis.set_ticks_position('top')
    else:
        plt.gca().xaxis.set_ticks([])

    plt.gca().tick_params(axis='y', which='major', pad=1)
    plt.gca().tick_params(axis='x', which='major', pad=1)
        
    if title is None:
        title = ""
        if log_z:
            title += "log "
        title += variable
        title += " for (" + filters + ")"
    plt.title(title)
    

def do_grid(viz_data, dimensions,variable,
            log_x=True,log_y=True,log_z=True,plot_data_points=False,
            xlim=None,ylim=None,cmap="viridis",
            vmin=None,vmax=None,
            hide_spine=None,hide_ylabel=False,
            xlabel_transform=None,
            xticks=None,yticks=None,
            plot_landmarks=False,
            landmarks=None,
            row_label_as_title=False,
            grid_x_values=None,grid_y_values=None):
    for key, value in dimensions.items():
            if value == "**GX**":
                grid_x = key
            elif value == "**GY**":
                grid_y = key
    if grid_x_values == None:
        grid_x_values = sorted(viz_data[grid_x].unique())
    if grid_y_values == None:
        grid_y_values = sorted(viz_data[grid_y].unique())

    grid_x_len = len(grid_x_values)
    grid_y_len = len(grid_y_values)

    for grid_y_idx in range(grid_y_len):
        for grid_x_idx in range(grid_x_len):
            plt.subplot(grid_y_len, grid_x_len, grid_y_idx*grid_x_len+grid_x_idx+1)
            do_viz(viz_data,
                dimensions = dict(dimensions, **{grid_x:grid_x_values[grid_x_idx],
                                                 grid_y:grid_y_values[grid_y_idx]}),
                variable=variable,
                log_x=log_x,log_y=log_y, log_z=log_z, title='',
                plot_data_points=plot_data_points, x_label=False, y_label=False,
                spines=(['left' if grid_x_idx==0 and hide_spine != "left" else '' ]+
                        ['right' if grid_x_idx==grid_x_len-1 and hide_spine != "right" else '' ]+
                        ['bottom' if grid_y_idx==grid_y_len-1 else '' ]+
                        ['top' if False and grid_y_idx==0 else '' ]),
                xlim=xlim,ylim=ylim,
                xticks=xticks,
                yticks=yticks,
                cmap=cmap,
                vmin=vmin, vmax=vmax,
                plot_landmarks=plot_landmarks,
                landmarks=landmarks)

            # Left column, show grid_y labels
            if grid_x_idx == 0 and not hide_ylabel:
                if row_label_as_title:
                    title = grid_y_values[grid_y_idx]
                    if title == '294_satellite_image':
                        title = '294_satellite\n_image'
                    if title == "wine_quality_white":
                        title = 'wine_quality\n_white'
                    if hide_spine != "left":
                        plt.title(title,x=-0.01,y=0.9,loc='right')
                        label = [k for k,v in dimensions.items() if v=="**Y**"][0]
                        if label == "epoch":
                            label = "Epoch"
                        plt.ylabel(label, labelpad=5)
                else:
                    plt.ylabel(grid_y_values[grid_y_idx])

            if grid_x_idx==grid_x_len-1 and hide_spine != "right":
                label = [k for k,v in dimensions.items() if v=="**Y**"][0]
                if label == "epoch":
                    label = "Epoch"
                plt.ylabel(label, labelpad=2)
                plt.gca().yaxis.set_label_position("right")


            #  bottom, show grid_y labels
            if grid_y_idx == grid_y_len-1:
                if row_label_as_title:
                    label = [k for k,v in dimensions.items() if v=="**X**"][0]
                    if label == "num_free_parameters":
                        label = "# Parameters"
                    plt.xlabel(label, labelpad=1)
                else:
                    xlabel = grid_x_values[grid_x_idx]
                    if xlabel_transform:
                        xlabel = xlabel_transform(xlabel)
                    plt.xlabel(xlabel)

            if grid_y_idx == 0:
                if row_label_as_title:
                    xlabel = grid_x_values[grid_x_idx]
                    if xlabel_transform:
                        xlabel = xlabel_transform(xlabel)
                    plt.title(xlabel)
                else:
                    plt.title("Column title")

    plt.tight_layout()

    if row_label_as_title:
        plt.subplots_adjust(top=0.95,bottom=0.06,left=0.12, hspace=0.2, wspace=0.1)