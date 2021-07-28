class PerfectMatch:
    query_id = ""
    query_seq = ""
    query_start = 0
    query_end = 0
    hit_id = ""
    hit_seq = ""
    hit_start = 0
    hit_end = 0
    match_seq = ""
    match_midline = ""

    def __init__(self, query_id: str, query_seq: str, query_start: int, query_end: int, hit_id: str, hit_seq: str, hit_start: int, hit_end: str, match_seq: str, match_midline: str):
        self.query_id = query_id
        self.query_seq = query_seq
        self.query_start = query_start
        self.query_end = query_end
        self.hit_id = hit_id
        self.hit_seq = hit_seq
        self.hit_start = hit_start
        self.hit_end = hit_end
        self.match_seq = match_seq
        self.match_midline = match_midline
    
    def get_query_id(self):
        return self.query_id
    
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
    
    def get_match_seq(self):
        return self.match_seq

    def get_match_midline(self):
        return self.match_midline

    def to_dict(self):
        info = {
            "Query_id": self.query_id,
            "Query_seq": self.query_seq,
            "Query_start": self.query_start,
            "Query_end": self.query_end,
            "Hit_id": self.hit_id,
            "Hit_seq": self.hit_seq,
            "Hit_start": self.hit_start,
            "Hit_end": self.hit_end,
            "Match_seq": self.match_seq,
            "Match_mid": self.match_midline
        }
        return info
    
    