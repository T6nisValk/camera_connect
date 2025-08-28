    def run(self):
        try:
            self.started_work.emit()
            total_files = self.count_files()
            self.file_count.emit(total_files)
            for i in range(1, total_files + 1):
                self.progress.emit(i)
                time.sleep(0.1)
            self.finished_work.emit()
        except Exception as e:
            self.error.emit(str(e))