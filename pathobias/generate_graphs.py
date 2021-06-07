import os
import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt
import yaml
import logging

sns.set_theme(style="darkgrid")

parser = argparse.ArgumentParser()

parser.add_argument("--config", type=str,
                    help="path to a config file.")

args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('%(name)s - [%(levelname)s] - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)


def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    lgd = ax.legend(handles, labels, loc=new_loc, title=title, bbox_to_anchor=(1.05, 1), **kws)
    return lgd


def main():
    with open(args.config, "r") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    file = cfg['file']
    tasks = cfg['tasks']
    bias = cfg['bias_source']
    outfolder = cfg['outfolder']
    format = cfg['format']

    df = pd.read_csv(file, sep=None, engine='python', keep_default_na=False, na_values=['', 'null'])
    for t in tasks:
        for b in bias:
            df[t] = df[t].astype('object')
            df[t] = df[t].fillna('NA')

            if b == 'N_patches':
                df[b] = df[b].astype('float64')
                fig, ax = plt.subplots()
                splot = sns.histplot(data=df[df[t] != 'NA'], x=b, hue=t, kde=True, log_scale=True, ax=ax)
                lgd = move_legend(ax, "upper left", prop={'size': 8})
            else:
                fig, ax = plt.subplots()
                splot = sns.histplot(data=df[df[t] != 'NA'], x=t, hue=b, multiple='stack', ax=ax, stat='count')
                lgd = move_legend(ax, "upper left", prop={'size': 8})

            nt = t.replace('/', '_')
            img_file = os.path.join(outfolder, f'Graph_{nt}_{b}{format}')
            fig.savefig(img_file, dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')
            logger.info(f'Saved figure {img_file}')


if __name__ == "__main__":
    main()
