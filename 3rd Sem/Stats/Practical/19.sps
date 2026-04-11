* Encoding: UTF-8.
* Practical 19: Friedman’s test (Alpha, Sigma, Gamma) with Grades I–IV as blocks.

GET DATA
  /TYPE=XLSX
  /FILE="C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Practical_19.xlsx"
  /SHEET=NAME  "Practical19"
  /READNAMES=on.
EXECUTE.
DATASET NAME data_for_19 WINDOW=FRONT.

DATASET ACTIVATE data_for_19.

NPAR TESTS
  /FRIEDMAN = Alpha Sigma Gamma.
