cd "D:\Users\praka\Desktop\csit\Practical sem 3"
//ssc install asdoc

clear
set more off
capture log close
log using practicalcsitsem3_3.log, replace

//Practical 1
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A sample of size 150 provided the mean of 47.5. 
//Can it be regarded as representative of population with mean 50 and standard deviation 12 at 5% level of significance. 
//Also find the 95% confidence limits for the population mean using the sample data.

ztesti 150 47.5 12 50

clear
//Practical 2
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two samples of size 30 each is selected. From two independent populations With variances 840 and 920 respectively. 
//Are the selected samples Have Equal means at 5% level of significance. 
//Also find 95% confidence limits for the difference of means. 
// use data in question 2

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical2.xlsx", sheet("Sheet1") firstrow

ztest x == y, unpaired sd1(840) sd2(920)
clear
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical2.xlsx", sheet("Sheet2") firstrow 
ztest value, by(grp) sd1(840) sd2(920)
clear

clear

//Practical 3
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A sample of size trout is selected from the population of which mean 1100 And standard deviation 275. 
//Following are the records of the sample selected. 
//Can the sample be regarded as the representative of parent population.
//use file practical 3

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical3.xlsx", sheet("Sheet1") firstrow

ztest x == 1100, sd(275)

clear


//Practical 4
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two samples of size 50 each are selected to test the proportion of the smokers among the proportion. 
//It is observed that 44% in the first population and 50% in the second samples are smokers. 
//Is the hypothesis of lesser smokers in first population is significant. 
//Also find the 95% confidence limits for the difference of proportion.

prtesti 50 .44 50 .5

clear


//Practical 5
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//The time (in minutes) spent by 10 randomly selected customers using internet in a cyber cafe are as follows;
//35 ,20 ,30 ,45 ,60 ,40 ,65 ,40 ,25 ,50
//Can you say average time spent by customers is more than 30 minutes at 5% level of significance?

//Test Hypothesis
//Null Hypothesis:mean=30
//Alternate Hypothesis: mean>30
//one sample t test is used
//Under null hypothesis H0, test statistic is 
//t = (mean-30)/S.E.

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

// create data table with variable name time in minutes
ttest time_in_min == 30
// t test for single sample with hypothesized mean 30
clear
// clear memory

//Practical 6
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Two kinds of manure were applied to sixteen one-hectare  plot, other condition remaining the
//same. The yields in quintals are given below:

//Manure I	18	20	36	50	49	36	34	49	41
//Manure II	29	28	26	35	30	44	46	
//Is there any significant difference between the mean yields? Use 5% level of significance.Also use Mann Whitney U test to give conclusion.

//Use file practical 6

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical6.xlsx", sheet("Sheet1") firstrow

// independent sample t-test
// using variable
ttest ManureI == ManureII, unpaired unequal
// using groups
clear
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical6.xlsx", sheet("Sheet2") firstrow
ttest value, by(type) unequal

// Mann Whitney U test
ranksum value, by(type)

clear


//Practical 7
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Memory capacity of 10 students was tested before and after training, 
//state whether the training was effective or not from the following scores;

//Roll No.	1	2	3	4	5	6	7	8	9	10
//Before training	12	14	11	8	7	10	3	0	5	6
//After training	15	16	10	7	5	12	10	2	3	8
//Use both parametric and non-parametric test of hypothesis to give conclusion.

//Working Expression

// Using Paired t test
//Test Hypothesis
//Null Hypothesis: H0: mean1 = mean2
//Alternate hypothesis: H1: mean1 < mean2
//Under null hypothesis , H0, test statistic is
//|t|=|(mean of difference)/S.E. of difference|
//Level of significance = alpha =(0.05)
//degrees of freedom = n-1 where n = no of pairs of observation
//critical value = tabulated t at defined level of significance and available df
//Decision: Reject H0 if calculated t is in critical region
//for p value approach
//pvalue=P(t<tcal) for left tailed test
//pvalue=P(t>tcal) for right tailed test
//pvalue=P(|t|>tcal) for two tailed test
//Decision: If pvalue> alpha, it is insignificant
//pvalue<= alpha, it is significant
//pvalue<0.001, it is highly significant
// working expression for Wilcoxon paired signed rank test --write yourself..........................

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical7.xlsx", sheet("Sheet1") firstrow

// paired t-test
ttest Beforetraining == Aftertraining

// Wilcoxon Signed Ranks test
signrank Beforetraining = Aftertraining


clear

//Practical 8
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Find confidence interval of mean assuming normal distribution for following data. height
//78	55	68	48	65	76	57	55	65	75	51	61
//68	67	76	78	71	56	57	67	58	51	50	58
//50	77	55	48	70	55	58	70	56	52	74	61
//69	76	61	68	78	56	78	57	66	66	74	66

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical8.xlsx", sheet("Sheet1") firstrow
// confidence interval of means
ci means x
// test of randomness using run tested
runtest x
summarize x, detail
ci mean x
runtest x
ksmirnov x = normalden( x ,63,9)
ksmirnov x = tden(46, x )

clear

//Practical 9
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Construct random data of size 5000 height of students categorized by gender. Considering minimum height of 120 cms. to 185 cms.
//a)   Draw a sample calculating appropriate sample size assuming the proportion of male and female are equal for 5 % desired margin of error.
//b)   Test the hypothesis of male and female are of equal in proportion for the population you have constructed.
//c)   Test the hypothesis of male are taller than female students at 5 % level of significance. 
//d)   If the sample size is 500 what will be the change in decision for above hypothesis.
//e)   Find the 95% confidence limits of proportion of gender and 95 % confidence limits for the difference of height for both cases of sample.
//note excel to construct the data file and conduct analysis in stata.

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical9.xlsx", sheet("Sheet1") firstrow

display "n=(1.96^2)*.5*.5/0.05^2 ="
display (1.96^2)*.5*.5/0.05^2

sample 385, count
save "D:\Users\praka\Desktop\csit\Practical sem 3\samplefile1.dta", replace
describe
summarize, detail

//b)
prtest gender == 0.5

//c)
ttest height, by(gender) unequal

clear

//d)
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\practical9.xlsx", sheet("Sheet1") firstrow
sample 500, count
save "D:\Users\praka\Desktop\csit\Practical sem 3\samplefile2.dta", replace
describe
prtest gender == 0.5
ttest height, by(gender) unequal

//e)
ci proportion gender
prtesti 385 0.496 500 0.498

clear


//Practical 10
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

import excel "D:\Users\praka\Desktop\csit\Practical sem 3\Practical 10.xlsx", sheet("Sheet2") firstrow clear
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
graph export "D:\Users\praka\Desktop\csit\Practical sem 3\Graph.jpg", as(jpg) name("Graph") quality(100)
rvfplot
graph export "D:\Users\praka\Desktop\csit\Practical sem 3\Graph1.jpg", as(jpg) name("Graph") quality(100)
rvpplot Initialweightpoundsx1
graph export "D:\Users\praka\Desktop\csit\Practical sem 3\Graph2.jpg", as(jpg) name("Graph") quality(100)

clear

//Practical 11
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//11.	The yield of treatments in different plots are as shown in the following plots. Carry out analysis.
//t₄    1401	t₃     2536	t₃     2459	t₁      2537	t₃     2827	t₁     2069
//t₂    2211	t₁     1797	t₄     1170	t₄     1516	t₄     2104	t₃     2385
//t₂    3366	t₁     2104	t₂     2591	t₃     2460	t₄     1077	t₂      2544
//(use data from excel after arranging)
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\Practical 11.xlsx", sheet("Sheet1") firstrow
oneway value treatment, bonferroni
//Kruskal Wallis test
kwallis value, by(treatment)
//if p value>= alpha, H0 is rejected, accept H0 otherwise
clear

//Practical 12
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//12.	The following table gives the result of the experiment on four varieties of a crop in 5 blocks of plot.
//          Block I                  Block II               Block III              Block IV              Block V
//A           32	B           33	D          30	A           35	C            36
//B           34	C           34	C           35	C            32	D            29
//C           31	A          34	B           36	B            37	A            37
//D           29	D          26	A           33	D           28	B            35
//Analyse the above result to test whether there is significant difference between yields of four varieties.
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\Practical 12.xlsx", sheet("Sheet1") firstrow
anova values Treatment Block
oneway value Treatment, bonferroni

clear

//Practical 13
di "$S_DATE $S_TIME"
display "`c(hostname)'"
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\Practical 13.xlsx", sheet("Sheet1") firstrow
anova Values Rows Column Treatment
oneway Values Treatment, bonferroni
clear


clear
//Practical 14
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

clear

clear
//Practical 15
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//Fit the appropriate distribution and test the goodness of fit of the constructed data using chi square test and K-S test for normality of following data. 
//x	frequency
//0	2
//1	8
//2	15
//3	40
//4	65
//5	55
//6	38
//7	12
//8	5
//9	2
input x frequency
0 2
1 8
2 15
3 40
4 65
5 55
6 38
7 12
8 5
9 2
end
generate trials = 9
//expand frequency
summarize x [fweight = frequency]
scalar p = r(mean)/trials
display "Estimated p= " p
summarize frequency
display r(sum)
generate totalf = r(sum)
generate expected_p = comb(trials,x) * p^x * (1-p)^(trials-x) 
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

clear

//Practical 16
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//A tobacco company claims that there is no relationship between smoking and lung ailments. To investigate the claims random sample of 300 males in age group of 40 to 50 is given medical test. The observed sample result is tabulated below:
//	Lung ailment	No lung ailment	Total
//Smokers	75	105	180
//No smokers	25	95	120
//Total	100	200	300
//On the basis of this information, can it be concluded that smoking and lung ailment are independent?
//Method 1
clear
tabi 75 105 \ 25 95, chi2 expected row col
//Method 2: Creating a Dataset and Then Analyzing
clear
input str8 Smokers str8 Lung_infection count
"Yes" "yes" 75
"Yes" "no" 105
"No" "yes" 25
"No" "no" 95
end
expand count
tab Smoker Lung_infection, chi2 expected row col
clear




clear
//Practical 17
di "$S_DATE $S_TIME"
display "`c(hostname)'"
//In an experiment on immunization of cattle from tuberculosis, the following results were obtained.
//	Affected	Not affected
//Inoculated	2	10
//Not inoculated	6	6
//Examine whether the vaccine has an effect in controlling the disease. (Use Chi-square test and z test of proportion)
// disease (1=affected, 0=not_affected)
// vaccination (1=inoculated, 0=not_inoculated)
import excel "D:\Users\praka\Desktop\csit\Practical sem 3\Practical 17.xlsx", sheet("Sheet1") firstrow
tabulate disease vaccination, chi2
clear
//Method 1
clear
tabi 2 10 \ 6 6, chi2 expected row col
//Method 2: Creating a Dataset and Then Analyzing
clear
input str12 disease str8 vaccination count
"Infected" "Vac_yes" 2
"Infected" "Vac_no" 10
"Notinfected" "Vac_yes" 6
"Notinfected" "Vac_no" 6
end
expand count
tab disease vaccination, chi2 expected row col
clear

//Practical 18
di "$S_DATE $S_TIME"
display "`c(hostname)'"
sysuse auto
sum
describe
ttest price = 6000
ttest price, by(foreign)
ttest price ==7000
ttest price, by(foreign)
ttest price == weight, unpaired
ttesti 25 50 10 55
 //prtest price, by(foreign)
generate price_grp =price
replace price_grp=0 if price<5000
replace price_grp=1 if price>=5000
prtest price_grp, by(foreign)
sdtest price, by(foreign)
oneway foreign price
oneway foreign price, tab
oneway foreign price, bon
oneway foreign price, sid
tab mpg
generate mpg_grp=mpg
replace mpg_grp = 0 if mpg<20
replace mpg_grp = 1 if mpg>=20 & mpg <30
replace mpg_grp = 2 if mpg>=30 & mpg <40
replace mpg_grp = 3 if mpg>=40
anova price foreign mpg_grp
ranksum price, by(foreign)
runtest price
kwallis price, by(mpg)
bitest foreign == 0.5
corr price mpg rep78 headroom trunk weight length turn displacement gear_ratio foreign
regress price weight length turn displacement
vif 
regress price weight turn displacement
regress price turn displacement
regress price displacement
regress price displacement foreign
predict y
predict resid, residuals
pnorm resid
qnorm resid
rvfplot
pwcorr price y
pwcorr price y,sig
correlate price y
spearman price mpg foreign


log close
