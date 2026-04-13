select *
from layoffs_staging;

#Pre-step: create staging table so you dont use the raw data
#1: remove duplicates -- this data does not have duplicates, if it did, I would need to identify the key coulunms that 
	#would demonstrate a duplicate row-- the fields would be company, location, date, and total_laid_off
    #partition by these columns and add the row number, the duplicates will have two as the row number
    #if duplicates were found, create a second staging table with the row number as an extra column, filter out the rows with a two, and delete them
    
#2: standardizing
	#remove whitespace with trim
    #combine categories that need to be -- consider whether differing category names could lead to duplicate rows

select distinct industry
from layoffs_staging
order by 1;

select distinct location
from layoffs_staging
order by 1;

select distinct country
from layoffs_staging
order by 1;
#period at end of united states
select distinct country, Trim(trailing "." from country)
from layoffs_staging
order by 1;

update layoffs_staging
set country = Trim(trailing "." from country)
where country like "United States%";

#format date
select `date`, str_to_date(`date`, '%m/%d/%Y')
from layoffs_staging;

update layoffs_staging
set `date`= str_to_date(`date`, '%m/%d/%Y');

alter table layoffs_staging
modify column `date` date;

select *
from layoffs_staging;

#3: deal with blanks and nulls
#looking at the data, if both the percentage and total laid off are null, they do not give use information and will be deleted

#Airbnb and Ballys are blank, so check if the companies pop up else where
select *
from layoffs_staging
where industry is null 
or industry = '';

#checks if we can populate based on another row of the same company-- in this case, we cannot. 
	#I should do research on what the company is/does and fill in accordingly
select *
from layoffs_staging st1
join layoffs_staging st2
	on st1.company=st2.company
    and st1.location=st2.location
where (st1.company is null or st1.company = '')
	and st2.company is not null;

#now move on to deleting the rows with pissing totals and percentages
select *
from layoffs_staging
where (total_laid_off is null or total_laid_off = '')
and (percentage_laid_off is null or percentage_laid_off = '');

delete
from layoffs_staging
where (total_laid_off is null or total_laid_off = '')
and (percentage_laid_off is null or percentage_laid_off = '');
#extra notes:
	#based on the information, the most important measurement is the total_laid_off, most everything else is categorical-- the percentage does not do much with out the company size. 
    #The other important measurement is the funds raised. It may be helpful to delete rows with both these measurements missing.

#if a clomun need to be removed, alter the table with drop

select *
from layoffs_staging;




    