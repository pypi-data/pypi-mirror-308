from scripts.check import check_clean


class Worker(object):
    def __init__(self):
        pass

    def before_run(self):
        check_clean()

    def after_run(self):
        pass

    def main(self):
        """user implement this"""
        pass

    def run(self):
        self.before_run()
        self.main()
        self.after_run()
