import glob
import matplotlib.pyplot as plt
import brewer2mpl
from features import *
from random import randint
import seaborn as sns
import numpy as np


def plot_grid(grid, count=False):
    # plt.style.use('ggplot')

    # brewer2mpl.get_map args: set name  set type  number of colors
    # bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)

    # cmap = 'plasma'
    # cmap = 'inferno'
    # cmap = 'magma'
    # cmap = 'viridis'

    if count:
        ax = sns.heatmap(grid.count_grid, linewidth=0.5, vmin=0, vmax=np.max(grid.count_grid))
    else:
        ax = sns.heatmap(grid.val_grid, linewidth=0.5, vmin=0, vmax=1)
    fig = ax.get_figure()
    ax.axes.set_xlabel(grid.feature_b.title, fontsize=14)
    ax.axes.set_ylabel(grid.feature_a.title, fontsize=14)
    ax.axes.set_xticklabels(np.arange(int(grid.feature_b.range[0]), int(grid.feature_b.range[1]), int((grid.feature_b.range[1] - grid.feature_b.range[0])/grid.k)))
    ax.axes.set_yticklabels(reversed(np.arange(int(grid.feature_a.range[0]), int(grid.feature_a.range[1]),
                                      int((grid.feature_a.range[1] - grid.feature_a.range[0]) / grid.k))))
    fig.show()
    fig.savefig('feature_map_' + grid.title.lower() + ("_count" if use_count else "") + '.pdf')


class MockPlayer:

    def __init__(self, player_id):
        self.player_id = player_id
        self.apm = randint(0, 500)
        self.mmr = randint(500, 3000)
        self.won = 1 if randint(0, self.apm*2+self.mmr) > 250*2+1000 else 0


class MockGame:

    def __init__(self, game_id):
        self.game_id = game_id
        self.players = [MockPlayer(100000+game_id), MockPlayer(200000+game_id+1)]


# Mock data
games = []
for i in range(10000):
    games.append(MockGame(i))

win_dict = {}
for game in games:
    for player in game.players:
        win_dict[player.player_id] = 1 if player.won else 0

# Save data as cache

# Make a grid for each feature combination
feature_apm = FeatureDimAPM(games)
feature_mmr = FeatureDimMMR(games)

# Make grid
grid = FeatureGrid(feature_apm, feature_mmr, win_dict)

for use_count in [False, True]:
    plot_grid(grid, count=use_count)
