def turun(q, qmin, qmax):
    return (qmax-q)/(qmax-qmin)

def naik(q, qmin, qmax):
    return(q-qmin)/(qmax-qmin)

class Permintaan():
    minimal = 250
    maximal = 3670
    median = 850

    def down(self, q):
        if q >= self.median:
            return 0
        elif q <= self.minimal:
            return 1
        else :
            return turun(q, self.minimal, self.median)
    
    def up(self, q):
        if q >= self.maximal:
            return 1
        elif q <= self.median:
            return 0
        else :
            return naik(q, self.median  , self.maximal)
    
    def consistent(self, q):
        if q >= self.maximal or q <= self.minimal:
            return 0
        elif self.minimal < q < self.median:
            return naik(q, self.minimal, self.median)
        elif self.median < q < self.maximal:
            return turun(q, self.median, self.maximal)
        else :
            return 1

class Persediaan():
    minimal = 115
    maximal = 600

    def sedikit(self, w):
        if w >= self.maximal:
            return 0
        elif w <= self.minimal:
            return 1
        else :
            return turun(w, self.minimal, self.maximal)
    
    def banyak(self, w):
        if w >= self.maximal:
            return 1
        elif w <= self.minimal:
            return 0
        else :
            return naik(w, self.minimal, self.maximal)

class Produksi():
    minimal = 1000
    maximal = 5400
    permintaan = 0
    persediaan = 0

    def _kurang(self, e):
        return self.maximal - e*(self.maximal - self.minimal)

    def _tambah(self, e):
        return e*(self.maximal - self.minimal) + self.minimal

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        #==================
        q1 = min(pmt.down(self.permintaan), psd.banyak(self.persediaan))
        e1 = self._kurang(q1)
        result.append((q1, e1))
        #===================
        q2 = min(pmt.down(self.permintaan), psd.sedikit(self.persediaan))
        e2 = self._kurang(q2)
        result.append((q2, e2))
        #====================
        q3 = min(pmt.up(self.permintaan), psd.banyak(self.persediaan))
        e3 = self._tambah(q3)
        result.append((q3, e3))
        #===================
        q4 = min(pmt.up(self.permintaan), psd.sedikit(self.persediaan))
        e4 = self._kurang(q4)
        result.append((q4, e4))
        #====================
        q5 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        e5 = self._tambah(q5)
        result.append((q5, e5))
        #=====================
        q6 = min(pmt.consistent(self.permintaan), psd.sedikit(self.persediaan))
        e6 = self._kurang(q6)
        result.append((q6, e6))

        return result

    def defuzifikasi(self, data_inferensi=[]):
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        has_q_e = 0
        has_q = 0
        for data in data_inferensi:
            has_q_e += data[0] * data[1]
            has_q += data[0]
        return has_q_e/has_q