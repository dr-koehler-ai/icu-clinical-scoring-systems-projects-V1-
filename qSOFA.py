def qsofa_score(Blutdruck, Atemfrequenz, GCS):
  score = 0

  if Blutdruck < 100:
      score += 1
  if Atemfrequenz > 22:
      score += 1
  if GCS < 15:
      score += 1

  return score

def classify_sepsis(score):
    if score >= 2:
        return "High risk"
    else:
        return "Low risk"

patients = [(110, 20,15), (90,20,15), (80,30,11)]

for p in patients:
    score = qsofa_score(*p)
    print(classify_sepsis(score))