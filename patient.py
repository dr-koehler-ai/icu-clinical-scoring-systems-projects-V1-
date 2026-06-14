class Patient:

    def __init__(
        self,
        name,

        # Respiratorisch
        pao2_fio2,
        respiratory_rate,
        ventilated,
        pao2,

        # Hämodynamik
        map_value,
        heartrate,
        zvd,
        dopamine,
        dobutamine,
        norepi,
        epi,

        # Neurologisch
        gcs,

        # Niere
        creatinine,
        dialysis,

        # Leber
        bili,

        # Hämatologie
        platelets,
        hematocrit,
        wbc,

        # Elektrolyte
        sodium,
        potassium,

        # Säure-Basen
        ph,

        # Sonstiges
        temperature,
        age,

        # Chronisch
        severe_chronic_disease=False
    ):
        self.name = name

        self.pao2_fio2 = pao2_fio2
        self.respiratory_rate = respiratory_rate
        self.ventilated = ventilated
        self.pao2 = pao2

        self.map_value = map_value
        self.heartrate = heartrate
        self.zvd = zvd

        self.dopamine = dopamine
        self.dobutamine = dobutamine
        self.norepi = norepi
        self.epi = epi

        self.gcs = gcs

        self.creatinine = creatinine
        self.dialysis = dialysis

        self.bili = bili

        self.platelets = platelets
        self.hematocrit = hematocrit
        self.wbc = wbc

        self.sodium = sodium
        self.potassium = potassium

        self.ph = ph

        self.temperature = temperature
        self.age = age

        self.severe_chronic_disease = severe_chronic_disease

class ClinicalScores:

    def __init__(self, patient):
        self.patient = patient


# ---------------- SOFA ----------------

class SofaScore(ClinicalScores):

    def calculate(self):
        return self.total_sofa()

    def sofa_resp(self):
        if self.patient.pao2_fio2 >= 400:
            return 0
        elif self.patient.pao2_fio2 >= 300:
            return 1
        elif self.patient.pao2_fio2 >= 200:
            return 2
        elif self.patient.pao2_fio2 >= 100:
            return 3 if self.patient.ventilated else 2
        else:
            return 4

    def sofa_cardiovascular(self):
        if (
            self.patient.map_value >= 70
            and self.patient.dopamine == 0
            and self.patient.dobutamine == 0
            and self.patient.norepi == 0
            and self.patient.epi == 0
        ):
            return 0
        elif self.patient.map_value < 70:
            return 1
        elif (0 < self.patient.dopamine <= 5 or self.patient.dobutamine > 0):
            return 2
        elif (
            5 < self.patient.dopamine <= 15
            or 0 < self.patient.norepi <= 0.1
            or 0 < self.patient.epi <= 0.1
        ):
            return 3
        else:
            return 4

    def sofa_renal(self):
        if self.patient.dialysis:
            return 4
        elif self.patient.creatinine < 1.2:
            return 0
        elif self.patient.creatinine < 2:
            return 1
        elif self.patient.creatinine < 3.5:
            return 2
        elif self.patient.creatinine < 5:
            return 3
        else:
            return 4

    def sofa_platelets(self):
        if self.patient.platelets >= 150:
            return 0
        elif self.patient.platelets >= 100:
            return 1
        elif self.patient.platelets >= 50:
            return 2
        elif self.patient.platelets >= 20:
            return 3
        else:
            return 4

    def sofa_bilirubin(self):
        if self.patient.bili < 1.2:
            return 0
        elif self.patient.bili < 2:
            return 1
        elif self.patient.bili < 6:
            return 2
        elif self.patient.bili < 12:
            return 3
        else:
            return 4

    def sofa_gcs(self):
        if self.patient.gcs == 15:
            return 0
        elif self.patient.gcs >= 13:
            return 1
        elif self.patient.gcs >= 10:
            return 2
        elif self.patient.gcs >= 6:
            return 3
        else:
            return 4

    def total_sofa(self):
        return (
            self.sofa_resp()
            + self.sofa_platelets()
            + self.sofa_bilirubin()
            + self.sofa_cardiovascular()
            + self.sofa_gcs()
            + self.sofa_renal()
        )


# ---------------- qSOFA ----------------

class qSOFA(ClinicalScores):

    def calculate(self):
        score = 0

        if self.patient.map_value <= 100:
            score += 1
        if self.patient.respiratory_rate > 22:
            score += 1
        if self.patient.gcs < 15:
            score += 1

        return score


# ---------------- MODS ----------------

class MODS(ClinicalScores):

    def calculate(self):
        return self.total_mods()

    def mods_resp(self):
        if self.patient.pao2_fio2 >= 300:
            return 0
        elif self.patient.pao2_fio2 >= 226:
            return 1
        elif self.patient.pao2_fio2 >= 152:
            return 2
        elif self.patient.pao2_fio2 >= 76:
            return 3 if self.patient.ventilated else 2
        else:
            return 4

    def mods_cardiovascular(self):
        par = (self.patient.heartrate * self.patient.zvd) / self.patient.map_value

        if par < 10:
            return 0
        elif par < 15:
            return 1
        elif par < 20:
            return 2
        elif par < 30:
            return 3
        else:
            return 4

    def mods_renal(self):
        if self.patient.creatinine <= 1.1:
            return 0
        elif self.patient.creatinine <= 2.3:
            return 1
        elif self.patient.creatinine <= 4.0:
            return 2
        elif self.patient.creatinine <= 5.7:
            return 3
        else:
            return 4

    def mods_platelets(self):
        if self.patient.platelets >= 120:
            return 0
        elif self.patient.platelets >= 81:
            return 1
        elif self.patient.platelets >= 51:
            return 2
        elif self.patient.platelets >= 21:
            return 3
        else:
            return 4

    def mods_bilirubin(self):
        if self.patient.bili <= 1.2:
            return 0
        elif self.patient.bili <= 3.5:
            return 1
        elif self.patient.bili <= 7.0:
            return 2
        elif self.patient.bili <= 14.0:
            return 3
        else:
            return 4

    def mods_gcs(self):
        if self.patient.gcs == 15:
            return 0
        elif self.patient.gcs >= 13:
            return 1
        elif self.patient.gcs >= 10:
            return 2
        elif self.patient.gcs >= 7:
            return 3
        else:
            return 4

    def total_mods(self):
        return (
            self.mods_resp()
            + self.mods_platelets()
            + self.mods_bilirubin()
            + self.mods_cardiovascular()
            + self.mods_gcs()
            + self.mods_renal()
        )


# ---------------- APACHE II ----------------

class APACHE2(ClinicalScores):

    def calculate(self):
        return (
            self.apache_temperature()
            + self.apache_map()
            + self.apache_heart_rate()
            + self.apache_resp_rate()
            + self.apache_pao2()
            + self.apache_ph()
            + self.apache_sodium()
            + self.apache_potassium()
            + self.apache_creatinine()
            + self.apache_hematocrit()
            + self.apache_wbc()
            + self.apache_gcs()
            + self.apache_age()
            + self.apache_chronic()
        )

    def apache_temperature(self):
        t = self.patient.temperature
        if 36 <= t <= 38.4:
            return 0
        elif 34 <= t <= 35.9 or 38.5 <= t <= 38.9:
            return 1
        elif 32 <= t <= 33.9:
            return 2
        elif 30 <= t <= 31.9 or 39 <= t <= 40.9:
            return 3
        else:
            return 4

    def apache_resp_rate(self):
        rr = self.patient.respiratory_rate
        if 12 <= rr <= 24:
            return 0
        elif 10 <= rr <= 11 or 25 <= rr <= 34:
            return 1
        elif 6 <= rr <= 9 or rr >= 35:
            return 2
        else:
            return 4

    def apache_pao2(self):
        p = self.patient.pao2
        if p >= 80:
            return 0
        elif 60 <= p < 80:
            return 1
        elif 55 <= p < 60:
            return 3
        else:
            return 4

    def apache_map(self):
        m = self.patient.map_value
        if 70 <= m <= 109:
            return 0
        elif 50 <= m <= 69:
            return 2
        else:
            return 4

    def apache_heart_rate(self):
        hr = self.patient.heartrate
        if 70 <= hr <= 109:
            return 0
        elif 55 <= hr <= 69 or 110 <= hr <= 139:
            return 2
        else:
            return 4

    def apache_creatinine(self):
        c = self.patient.creatinine
        if c < 1.5:
            return 0
        elif c <= 1.9:
            return 2
        elif c <= 3.4:
            return 3
        else:
            return 4

    def apache_ph(self):
        ph = self.patient.ph
        if 7.33 <= ph <= 7.49:
            return 0
        elif 7.25 <= ph <= 7.32 or 7.50 <= ph <= 7.59:
            return 2
        elif 7.15 <= ph <= 7.24:
            return 3
        else:
            return 4

    def apache_sodium(self):
        na = self.patient.sodium
        if 130 <= na <= 149:
            return 0
        elif 120 <= na <= 129 or 150 <= na <= 154:
            return 2
        elif 111 <= na <= 119 or 155 <= na <= 159:
            return 3
        else:
            return 4

    def apache_potassium(self):
        k = self.patient.potassium
        if 3.5 <= k <= 5.4:
            return 0
        elif 3.0 <= k <= 3.4 or 5.5 <= k <= 5.9:
            return 1
        elif 2.5 <= k <= 2.9 or 6.0 <= k <= 6.9:
            return 3
        else:
            return 4

    def apache_hematocrit(self):
        h = self.patient.hematocrit
        if 30 <= h <= 45:
            return 0
        elif 20 <= h <= 29 or 46 <= h <= 49:
            return 2
        else:
            return 4

    def apache_wbc(self):
        w = self.patient.wbc
        if 3 <= w <= 14.9:
            return 0
        elif 1 <= w <= 2.9 or 15 <= w <= 19.9:
            return 2
        else:
            return 4

    def apache_gcs(self):
        return 15 - self.patient.gcs

    def apache_age(self):
        a = self.patient.age
        if a <= 44:
            return 0
        elif a <= 54:
            return 2
        elif a <= 64:
            return 3
        elif a <= 74:
            return 5
        else:
            return 6

    def apache_chronic(self):
        return 5 if self.patient.severe_chronic_disease else 0

# ---------------- DASHBOARD ----------------

class ClinicalDashboard:

    def __init__(self, patient, scores):
        self.patient = patient
        self.scores = scores

    def generate_report(self):
        print(f"Patient: {self.patient.name}")

        for score in self.scores:
            print(f"{score.__class__.__name__}: {score.calculate()}")


# ---------------- TEST ----------------

patient_1 = Patient(
    name="Max Mustermann",
    pao2_fio2=120,
    respiratory_rate=30,
    ventilated=True,
    pao2=65,
    map_value=65,
    heartrate=120,
    zvd=8,
    dopamine=0,
    dobutamine=0,
    norepi=0.2,
    epi=0,
    gcs=10,
    creatinine=3.0,
    dialysis=True,
    bili=4.0,
    platelets=80,
    hematocrit=28,
    wbc=18,
    sodium=148,
    potassium=5.8,
    ph=7.28,
    temperature=39.2,
    age=72,
    severe_chronic_disease=True
)

dashboard = ClinicalDashboard(
    patient_1,
    [
        SofaScore(patient_1),
        MODS(patient_1),
        qSOFA(patient_1),
        APACHE2(patient_1)
    ]
)

dashboard.generate_report()