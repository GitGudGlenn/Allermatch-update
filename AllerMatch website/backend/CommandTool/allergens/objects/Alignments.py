class Alignments:
    query_id = ""
    query_window = ""
    query_seq = ""
    query_start = 0
    query_end = 0
    hit_id = ""
    hit_seq = ""
    hit_start = 0
    hit_end = 0
    midline = ""
    alignment_string = ""
    formatted_alignment = ""
    no_slices = 1
    window_identities = {}

    def __init__(self, query_id: str, query_window: str, query_seq: str, query_start: int, query_end: int, hit_id: str, hit_seq: str, hit_start: int, hit_end: int, 
                midline: str, alignment_string: str, formatted_alignment: str, no_slices: int, window_identities: dict):
        self.query_id = query_id
        self.query_window = query_window
        self.query_seq = query_seq
        self.query_start = query_start
        self.query_end = query_end
        self.hit_id = hit_id
        self.hit_seq = hit_seq
        self.hit_start = hit_start
        self.hit_end = hit_end
        self.midline = midline
        self.alignment_string = alignment_string
        self.formatted_alignment = formatted_alignment
        self.no_slices = no_slices
        self.window_identities = window_identities
    

    def get_query_id(self):
        return self.query_id
    
    def get_query_window(self):
        return self.query_window

    def get_query_seq(self):
        return self.query_seq
    
    def get_query_start(self):
        return self.query_start

    def get_query_end(self):
        return self.query_end

    def get_hit_id(self):
        return self.hit_id
    
    def get_hit_seq(self):
        return self.hit_seq

    def get_hit_start(self):
        return self.hit_start

    def get_hit_end(self):
        return self.hit_end
    
    def get_midline(self):
        return self.midline
    
    def get_alignment(self):
        return self.alignment_string
    
    def set_alignment(self, value):
        self.alignment_string = value
    
    def get_formatted_alignment(self):
        return self.formatted_alignment
    
    def set_formatted_alignment(self, value):
        self.formatted_alignment = value
    
    def get_no_slices(self):
        return self.no_slices
    
    def get_window_identities(self):
        return self.window_identities

    def to_dict(self):
        info = {
            "Query_id": self.query_id,
            "Query_window": self.query_window,
            "Query_seq": self.query_seq,
            "Query_start": self.query_start,
            "Query_end": self.query_end,
            "Hit_id": self.hit_id,
            "Hit_seq": self.hit_seq,
            "Hit_start": self.hit_start,
            "Hit_end": self.hit_end,
            "Midline": self.midline,
            "Alignment": self.alignment_string,
            "Formatted_align": self.formatted_alignment,
            "No_slices": self.no_slices,
            "Window_identities": self.window_identities
        }
        return info
