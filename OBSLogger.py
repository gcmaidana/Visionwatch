"""
@author: Gean Maidana Dollanarte
"""

import os

class OBSLogger:
    '''
    This class handles adding a win or loss to the record text file, as well as getting the number of wins and losses
    when we want to add to a given number of wins or losses

    We only want one instance of this class since this is the class that
    tracks our record
    '''
    _instance = None

    @staticmethod
    def get_instance(path):
        if OBSLogger._instance is None:
            OBSLogger._instance = OBSLogger(path)
        return OBSLogger._instance

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write("0-0")

    def add_win(self):
        wins, losses = self._get_record()
        wins += 1
        self._update_record(wins, losses)

    def add_loss(self):
        wins, losses = self._get_record()
        losses += 1
        self._update_record(wins, losses)


    def get_num_wins(self):
        return self._get_record()[0]

    def get_num_losses(self):
        return self._get_record()[1]

    def _get_record(self):
        with open(self.path, 'r') as f:
            record = f.read().strip().split('-')
        return [int(record[0][:-1]), int(record[1][:-1])]

    def _update_record(self, wins, losses):
        with open(self.path, 'w') as f:
            f.write(f"{wins}W-{losses}L")