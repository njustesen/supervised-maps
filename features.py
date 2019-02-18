import numpy as np


class FeatureGrid:

    def __init__(self, feature_a, feature_b, win_dict, k=10):
        self.count_grid = np.zeros((k, k))
        self.val_grid = np.zeros((k, k))
        self.feature_a = feature_a
        self.feature_b = feature_b
        a_step = (feature_a.range[1] - feature_a.range[0]) / k
        b_step = (feature_b.range[1] - feature_b.range[0]) / k
        for a in range(k):
            a_min = feature_a.range[0] + a_step * a
            a_max = a_min + a_step
            for b in range(k):
                b_min = feature_b.range[0] + b_step * b
                b_max = b_min + b_step
                count = 0
                val = []
                for player_id in feature_a.axis:
                    pos_a = feature_a.axis[player_id]
                    pos_b = feature_b.axis[player_id]
                    if a_min <= pos_a <= a_max and b_min <= pos_b <= b_max:
                        self.count_grid[k-a-1][b] += 1
                        val.append(win_dict[player_id])
                self.val_grid[k-a-1][b] = np.mean(val)
        self.k = k
        self.title = feature_a.title + " & " + feature_b.title


class FeatureDim:

    def __init__(self, games):
        self.title = "Not set"
        self.axis = {}
        for game in games:
            for player in game.players:
                self.axis[player.player_id] = self.get_value(game, player)
        self.range = self.set_range()

    def set_range(self):
        return [np.min(list(self.axis.values())), np.max(list(self.axis.values()))]

    def get_value(self, game, player):
        raise NotImplementedError("This method must be overridden by non-human subclasses")


class FeatureDimAPM(FeatureDim):

    def __init__(self, games):
        super().__init__(games)
        self.title = "APM"

    def get_value(self, game, player):
        return player.apm


class FeatureDimMMR(FeatureDim):

    def __init__(self, games):
        super().__init__(games)
        self.title = "MMR"

    def get_value(self, game, player):
        return player.mmr
