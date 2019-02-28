class Researcher:
    def __init__(self, first_name, last_name, crisid, orcid=None, scholar_url=None,
                 rg_url=None ):
        self.crisid = crisid
        self.first_name = first_name
        self.last_name = last_name
        self.scholar_url = scholar_url
        self.rg_url = rg_url
        self.orcid = orcid

        # set after initialization.
        self.scholar_data = None
        

    def to_dict(self):
        """ A representation of this Researcher as a dict following JSON
        naming conventions without None values (JSON-Compatible dict) """

        data = {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'crisID': self.crisid
        }

        if self.scholar_url:    data['googleScholarURL'] = self.scholar_url
        if self.rg_url:         data['researchGateURL'] = self.rg_url
        if self.orcid:          data['orcid'] = self.orcid
        if self.scholar_data:   data['scholarStats'] = self.scholar_data

        return data
    
    def to_dataframe(self):
        """ A representation of this Researcher as a dataframe following Pandas
        naming conventions without None values (Pandas-Compatible dict) """

        data = {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'crisID': self.crisid
        }

        if self.scholar_url:    data['googleScholarURL'] = self.scholar_url
        if self.rg_url:         data['researchGateURL'] = self.rg_url
        if self.orcid:          data['orcid'] = self.orcid

        if self.scholar_data == None:
            return data

        personal_data = self.scholar_data.get("personal_data", None)
        if personal_data:
            if personal_data.get("personal_info", None):   
                data['department'] = personal_data.get("personal_info", None)
            if personal_data.get("study_fields", None):   
                data['study_fields'] = ':'.join(personal_data.get("study_fields", None))
            
        stats = self.scholar_data.get("stats", None)
        if stats:
            citations = stats.get("citations", None) 
            if citations:   
                data['total_citations'] = citations.get("total", None)
                data['last5Years_citations'] = citations.get("last5Years", None)
            hIndex = stats.get("hIndex", None)
            if hIndex:   
                data['total_hIndex'] = hIndex.get("total", None)
                data['last5Years_hIndex'] = hIndex.get("last5Years", None)
            i10 = stats.get("i10", None)
            if i10:   
                data['total_i10'] = i10.get("total", None)
                data['last5Years_i10'] = i10.get("last5Years", None)
            citationsPerYear = stats.get("citationsPerYear", None)
            if citationsPerYear:
                data['citations_per_year'] = ';'.join([key+":"+val for key,val in citationsPerYear.items()])
        return data
    
    def search_name (self):
        trans = str.maketrans('áéíóúü','aeiouu')
        sname = (self.first_name +" "+ self.last_name.split(" ")[0]).translate(trans)
        return sname.encode('ascii', 'ignore').decode('ascii')