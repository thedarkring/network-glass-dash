class Render(object):

    def __init__(self):
        print('init')

    # Define custom render functions here

    def up_hours(self, uptime):
        uptime_hours = (int(uptime) / 360)
        return ('%s hours' % (uptime_hours))