import sys
from general import MessageService


class Progress():

    _annimations_ = ['-', '\\','|','/']
    
    def __init__(self, total, name=None):

        self._name = name
        
        self._total = total
        
        self._counter = 0        
    
    def progress(self, count):

        if self._counter == 0:
            msg  = 'Displaying progress'
            msg += ' of "%s":'%self._name if self._name else ''
            msg += ' ( Make coffee and be patient :-P ):'
            MessageService.info(msg)
            
        annimation_idx = self._counter % len(Progress._annimations_)
        annimation_icn = Progress._annimations_[annimation_idx]
        
        bar_len = 45
        filled_len = int(round(bar_len * count / float(self._total)))

        percents = round(100.0 * count / float(self._total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ... [%s]\r' % (bar, percents, '%', annimation_icn))

        sys.stdout.flush()
        
        self._counter += 1
