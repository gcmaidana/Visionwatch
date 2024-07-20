import os

class OBSLogger:
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
                f.write("0-0-0")

    def add_win(self):
        wins, losses, draws = self._get_record()
        wins += 1
        self._update_record(wins, losses, draws)

    def add_loss(self):
        wins, losses, draws = self._get_record()
        losses += 1
        self._update_record(wins, losses, draws)

    def add_draw(self):
        wins, losses, draws = self._get_record()
        draws += 1
        self._update_record(wins, losses, draws)

    def get_num_wins(self):
        return self._get_record()[0]

    def get_num_losses(self):
        return self._get_record()[1]

    def get_num_draws(self):
        return self._get_record()[2]

    def _get_record(self):
        with open(self.path, 'r') as f:
            record = f.read().strip().split('-')
        return list(map(int, record))

    def _update_record(self, wins, losses, draws):
        with open(self.path, 'w') as f:
            f.write(f"{wins}-{losses}-{draws}")