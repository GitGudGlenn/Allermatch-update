class Hit():
    query_id = ""
    query_seq = ""
    query_length = 0
    query_start = 0
    query_end = 0
    hit_id = ""
    hit_seq = ""
    hit_length = 0
    hit_start = 0
    hit_end = 0
    midline = ""
    alignment_string = ""
    formatted_alignment = ""
    bits = 0.0
    e_value = 0.0
    identity = 0.0
    similar = 0.0
    overlap = 0

    def __init__(self, query_id: str, query_seq: str, query_length: int, query_start: int, query_end: int, hit_id: str, hit_seq: str, hit_length: int, hit_start: int, hit_end: int, 
                midline: str, alignment_string: str, formatted_alignment: str, bits: float, e_value: float, identity: float, similar: float, overlap: int):
        self.query_id = query_id
        self.query_seq = query_seq
        self.query_length = query_length
        self.query_start = query_start
        self.query_end = query_end
        self.hit_id = hit_id
        self.hit_seq = hit_seq
        self.hit_length = hit_length
        self.hit_start = hit_start
        self.hit_end = hit_end
        self.midline = midline
        self.alignment_string = alignment_string
        self.formatted_alignment = formatted_alignment
        self.bits = bits
        self.e_value = e_value
        self.identity = identity
        self.similar = similar
        self.overlap = overlap

    def get_query_id(self):
        return self.query_id

    def get_query_seq(self):
        return self.query_seq
    
    def get_query_length(self):
        return self.query_length
    
    def get_query_start(self):
        return self.query_start

    def get_query_end(self):
        return self.query_end

    def get_hit_id(self):
        return self.hit_id
    
    def get_hit_seq(self):
        return self.hit_seq
    
    def get_hit_length(self):
        return self.hit_length

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
    
    def get_bits(self):
        return self.bits
    
    def get_e_value(self):
        return self.e_value
    
    def get_identity(self):
        return self.identity
    
    def get_similar(self):
        return self.similar
    
    def get_overlap(self):
        return self.overlap

    def to_dict(self):
        info = {
            "Query_id": self.query_id,
            "Query_seq": self.query_seq,
            "Query_length": self.query_length,
            "Query_start": self.query_start,
            "Query_end": self.query_end,
            "Hit_id": self.hit_id,
            "Hit_seq": self.hit_seq,
            "Hit_length": self.hit_length,
            "Hit_start": self.hit_start,
            "Hit_end": self.hit_end,
            "Midline": self.midline,
            "Alignment": self.alignment_string,
            "Formatted_align": self.formatted_alignment,
            "Bits": self.bits,
            "E_value": self.e_value,
            "Identity": self.identity,
            "Similar": self.similar,
            "Overlap": self.overlap,
        }
        return info