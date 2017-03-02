# Copyright (c) Trainline Limited, 2017. All rights reserved. See LICENSE.txt in the project root for license information.

import time

from progressbar import ProgressBar, FormatLabel, Timer, Bar, RotatingMarker, Percentage

class PatchProgress(object):
    widgets = []
    total_progress = 0
    
    def __init__(self):
        self.widgets = [RotatingMarker(), ' ', Percentage(), ' ', FormatLabel('Calculating patch requirements'), ' ', Bar(), ' ', Timer()]
        self.progress = ProgressBar(redirect_stdout=True, widgets=self.widgets, max_value=100)
        self.progress.update(1)

    def update(self, n_total, n_lc_updated, n_scaling_out, n_scaled_out, n_scaling_in, n_complete, *args):
        msg = '[Patching {0} ASGs]: {1} Scaling out, {2} Scaling in, {3} Complete'.format(n_total, n_scaling_out, n_scaling_in, n_complete)
        self.widgets[4] = FormatLabel(msg)
        t1 = (5 / n_total) * n_lc_updated
        t2 = (10 / n_total) * n_scaling_out
        t3 = (50 / n_total) * n_scaled_out
        t4 = (60 / n_total) * n_scaling_in
        t5 = (100 / n_total) * n_complete
        self.progress.update(t1 + t2 + t3 + t4 + t5)

