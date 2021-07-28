import tempfile

class Windows:
    query_id = ""
    query_window = ""
    sequence = ""

    
    def __init__(self, query_id, query_window, sequence):
        self.query_id = query_id
        self.query_window = query_window
        self.sequence = sequence

    
    def get_query_id(self):
        return self.query_id

    def get_query_window(self):
        return self.query_window

    def get_sequence(self):
        return self.sequence

    def to_dict(self):
        info = {
            "Query_id": self.query_id,
            "Query_window": self.query_window,
            "Sequence": self.sequence
        }
        return info
    
    def to_tempfile(self):
        tmp_window_file = tempfile.NamedTemporaryFile()
        with open(tmp_window_file.name, "w") as f:
            f.write(">query\n")
            f.write(self.sequence)
        return tmp_window_file