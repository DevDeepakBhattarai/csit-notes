cd "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats"
// ssc install asdoc
clear
set more off
capture log close
log using "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\output.log", replace

//Practical 1
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A sample of size 150 provided the mean of 47.5. 
//Can it be regarded as representative of population with mean 50 and standard deviation 12 at 5% level of significance. 
//Also find the 95% confidence limits for the population mean using the sample data.

ztesti 150 47.5 12 50



//Practical 2
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two samples of size 30 each is selected. From two independent populations With variances 840 and 920 respectively. 
//Are the selected samples Have Equal means at 5% level of significance. 
//Also find 95% confidence limits for the difference of means. 
// use data in question 2

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical2.xlsx", sheet("Sheet1") firstrow

ztest x == y, unpaired sd1(840) sd2(920)
clear

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical2.xlsx", sheet("Sheet2") firstrow 
ztest value, by(grp) sd1(840) sd2(920)




//Practical 3
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A sample of size trout is selected from the population of which mean 1100 And standard deviation 275. 
//Following are the records of the sample selected. 
//Can the sample be regarded as the representative of parent population.
//use file practical 3

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical3.xlsx", sheet("Sheet1") firstrow

ztest x == 1100, sd(275)

//Practical 4
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two samples of size 50 each are selected to test the proportion of the smokers among the proportion. 
//It is observed that 44% in the first population and 50% in the second samples are smokers. 
//Is the hypothesis of lesser smokers in first population is significant. 
//Also find the 95% confidence limits for the difference of proportion.

prtesti 50 .44 50 .5


//Practical 5
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//The time (in minutes) spent by 10 randomly selected customers using internet in a cyber cafe are as follows 35 ,20 ,30 ,45 ,60 ,40 ,65 ,40 ,25 ,50 Can you say average time spent by customers is more than 30 minutes at 5% level of significance?
input time_in_min
35
20
30
45
60
40
65
40
25
50
end
ttest time_in_min == 30

//Practical 6
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two kinds of manure were applied to sixteen one-hectare  plot, other condition remaining the
//same. The yields in quintals are given below:

//Manure I	18	20	36	50	49	36	34	49	41
//Manure II	29	28	26	35	30	44	46	
//Is there any significant difference between the mean yields? Use 5% level of significance.Also use Mann Whitney U test to give conclusion.

//Use file practical 6

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical6.xlsx", sheet("Sheet1") firstrow

// independent sample t-test
// using variable
ttest ManureI == ManureII, unpaired unequal
// using groups
clear
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical6.xlsx", sheet("Sheet2") firstrow
ttest value, by(type) unequal

// Mann Whitney U test
ranksum value, by(type)


//Practical 7
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical7.xlsx", sheet("Sheet1") firstrow

// paired t-test
ttest Beforetraining == Aftertraining

// Wilcoxon Signed Ranks test
signrank Beforetraining = Aftertraining

//Practical 8
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Find confidence interval of mean assuming normal distribution for following data. height
// 78	55	68	48	65	76	57	55	65	75	51	61
// 68	67	76	78	71	56	57	67	58	51	50	58
// 50	77	55	48	70	55	58	70	56	52	74	61
// 69	76	61	68	78	56	78	57	66	66	74	66
// 48   73  71  70  62  74  76  50  69  75  65  48

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical8.xlsx", sheet("Sheet1") firstrow
// confidence interval of means
ci means x
// test of randomness using run tested
runtest x
summarize x, detail
ksmirnov x = normalden( x ,63.88333,9.552871)
ksmirnov x = tden(59, x)


//Practical 9
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Construct random data of size 5000 height of students categorized by gender. Considering minimum height of 120 cms. to 185 cms.
//a)   Draw a sample calculating appropriate sample size assuming the proportion of male and female are equal for 5 % desired margin of error.
//b)   Test the hypothesis of male and female are of equal in proportion for the population you have constructed.
//c)   Test the hypothesis of male are taller than female students at 5 % level of significance. 
//d)   If the sample size is 500 what will be the change in decision for above hypothesis.
//e)   Find the 95% confidence limits of proportion of gender and 95 % confidence limits for the difference of height for both cases of sample.
//note excel to construct the data file and conduct analysis in stata.

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical9_random.xlsx", sheet("Sheet1") firstrow

display "n=(1.96^2)*.5*.5/0.05^2 ="
display (1.96^2)*.5*.5/0.05^2

sample 385, count
save "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical9_sample1.dta", replace
describe
summarize, detail

//b)
prtest gender == 0.5

//c)
ttest height, by(gender) unequal

clear

//d)
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical9_random.xlsx", sheet("Sheet1") firstrow
sample 500, count
save "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\practical9_sample2.dta", replace
describe
prtest gender == 0.5
ttest height, by(gender) unequal

//e)
ci proportion gender
prtesti 385 0.5090909 500 0.534

//Practical 10
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A developer of food for pig would like to determine what relationship exists among the age of a pig when it starts receiving a newly developed food supplement, the initial weight of the pig and the amount of weight it gains in a week period with the food supplement. The following information is the result of study of eight piglets.
//a.	Calculate the least square equation that best describes these three variables.
//b.	Calculate the standard error.
//c.	How much might we expect a pig to gain weight in a week with the food supplement if it were 9 weeks old and weighed 48 pounds? 
//d.	Find coefficient of determination. 
//e.	Test the significance of the regression Coefficients and overall regression. Conduct residual analysis. 
//f.	Test the multicollinearity between independent variables.
//g.	Find simple partial and multiple correlations. Test its significance.

import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Practical 10.xlsx", sheet("Sheet2") firstrow clear
//Regression analysis
regress Weightgainy Initialweightpoundsx1 Initialageweeksx2
//test of Multicollinearity
estat vif
//Calculation of value of dependent variable when x1 = 48 and x2 = 9
display _b[_cons] + _b[Initialweightpoundsx1]*48 + _b[Initialageweeksx2]*9
//Calculation of correlation matrix
corr Initialweightpoundsx1 Initialageweeksx2 Weightgainy
//Partial correlation matrix
pcorr Weightgainy Initialweightpoundsx1 Initialageweeksx2
pcorr Initialweightpoundsx1 Initialageweeksx2 Weightgainy
pcorr Initialageweeksx2 Weightgainy Initialweightpoundsx1
//Normal probability plot
pnorm Weightgainy
graph export "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Graph1.jpg", as(jpg) name("Graph") quality(100) replace
rvfplot
graph export "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Graph2.jpg", as(jpg) name("Graph") quality(100) replace
rvpplot Initialweightpoundsx1
graph export "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Graph3.jpg", as(jpg) name("Graph") quality(100) replace

//Practical 11
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//11.	The yield of treatments in different plots are as shown in the following plots. Carry out analysis.
//t₄    1401	t₃     2536	t₃     2459	t₁      2537	t₃     2827	t₁     2069
//t₂    2211	t₁     1797	t₄     1170	t₄     1516	t₄     2104	t₃     2385
//t₂    3366	t₁     2104	t₂     2591	t₃     2460	t₄     1077	t₂      2544
//(use data from excel after arranging)
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Practical 11.xlsx", sheet("Sheet1") firstrow
oneway value treatment, bonferroni
//Kruskal Wallis test
kwallis value, by(treatment)


//Practical 12
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//12.	The following table gives the result of the experiment on four varieties of a crop in 5 blocks of plot.
//          Block I                  Block II               Block III              Block IV              Block V
//A           32	B           33	D          30	A           35	C            36
//B           34	C           34	C           35	C            32	D            29
//C           31	A          34	B           36	B            37	A            37
//D           29	D          26	A           33	D           28	B            35
//Analyse the above result to test whether there is significant difference between yields of four varieties.
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Practical 12.xlsx", sheet("Sheet1") firstrow
anova values Treatment Block
oneway value Treatment, bonferroni


//Practical 13
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
import excel "C:\Users\deepak_bhattarai\OneDrive\Documents\Notes\3rd Sem\Stats\Practical\Practical 13.xlsx", sheet("Sheet1") firstrow
anova Values Rows Column Treatment
oneway Values Treatment, bonferroni

//Practical 14
clear
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//14.	Fit the appropriate distribution and test the goodness of fit of the constructed data using chi square test and K-S test for normality of following data. 
//x	frequency
//0	1112
//1	1308
//2	615
//3	90
//4	25
//5	5
//6	3
//7	1
//8	2
//9	2

input x frequency
0 1112
1 1308
2 615
3 90
4 25
5 5
6 3
7 1
8 2
9 2
end
generate trials = 9
//expand frequency
summarize x [fweight = frequency]
scalar m = r(mean)
display "Lambda= " m
summarize frequency
display r(sum)
generate totalf = r(sum)
generate expected_p = exp(-m) * ((m)^x)/exp(lngamma(x+1))
generate expected = expected_p * totalf
generate chi = (frequency - expected)^2 / expected
summarize chi
display "chi-square = " r(sum)
twoway (bar freq x, color(gs7)) ///
       (line expected x, lwidth(medthick))

	   
	   // ksmirnov test
summarize frequency	
generate empcdf = sum(freq)/totalf
summarize expected
generate bincdf = sum(expected)/totalf
generate diff = abs(empcdf - bincdf)
summarize diff
display "KS statistic D = " r(max)
display "D_alpha" = 1.36/sqrt(totalf)
//if KS statistic D > D_alpha,"reject H0", "H0 is accepted"


// //Practical 15
// clear
// di "$S_DATE $S_TIME"
// display "`c(hostname)'"
// //Fit the appropriate distribution and test the goodness of fit of the constructed data using chi square test and K-S test for normality of following data. 
// //x	frequency
// //0	2
// //1	8
// //2	15
// //3	40
// //4	65
// //5	55
// //6	38
// //7	12
// //8	5
// //9	2
// input x frequency
// 0 2
// 1 8
// 2 15
// 3 40
// 4 65
// 5 55
// 6 38
// 7 12
// 8 5
// 9 2
// end
// generate trials = 9
// //expand frequency
// summarize x [fweight = frequency]
// scalar p = r(mean)/trials
// display "Estimated p= " p
// summarize frequency
// display r(sum)
// generate totalf = r(sum)
// generate expected_p = comb(trials,x) * p^x * (1-p)^(trials-x) 
// generate expected = expected_p * totalf
// generate chi = (frequency - expected)^2 / expected
// summarize chi
// display "chi-square = " r(sum)
// twoway (bar freq x, color(gs7)) ///
//        (line expected x, lwidth(medthick))
//
//	   
// 	   // ksmirnov test
// summarize frequency	
// generate empcdf = sum(freq)/totalf
// summarize expected
// generate bincdf = sum(expected)/totalf
// generate diff = abs(empcdf - bincdf)
// summarize diff
// display "KS statistic D = " r(max)
// display "D_alpha" = 1.36/sqrt(totalf)
// //if KS statistic D > D_alpha,"reject H0", "H0 is accepted"
//
// //Practical 16
// clear
// di "$S_DATE $S_TIME"
// display "`c(hostname)'"
// //A tobacco company claims that there is no relationship between smoking and lung ailments. To investigate the claims random sample of 300 males in age group of 40 to 50 is given medical test. The observed sample result is tabulated below:
// //	Lung ailment	No lung ailment	Total
// //Smokers	75	105	180
// //No smokers	25	95	120
// //Total	100	200	300
// //On the basis of this information, can it be concluded that smoking and lung ailment are independent?
// input str8 Smokers str8 Lung_infection count
// "Yes" "yes" 75
// "Yes" "no" 105
// "No" "yes" 25
// "No" "no" 95
// end
// expand count
// tab Smoker Lung_infection, chi2 expected row col
//
//
// //Practical 17
// clear
// di "$S_DATE $S_TIME"
// display "`c(hostname)'"
// //In an experiment on immunization of cattle from tuberculosis, the following results were obtained.
// //	Affected	Not affected
// //Inoculated	2	10
// //Not inoculated	6	6
// //Examine whether the vaccine has an effect in controlling the disease. (Use Chi-square test and z test of proportion)
// // disease (1=affected, 0=not_affected)
// // vaccination (1=inoculated, 0=not_inoculated)
// input str12 disease str8 vaccination count
// "Infected" "Vac_yes" 2
// "Infected" "Vac_no" 10
// "Notinfected" "Vac_yes" 6
// "Notinfected" "Vac_no" 6
// end
// expand count
// tab disease vaccination, chi2 expected row col
// clear
// prtesti 12 0.1666667 12 0.5000000
// clear
//
//
//
//
