
select *
from layoffs_staging;

#initial thoughts: there is no total for how big the company is, so the percentage laid off is not gonna be the most helpful, the total will

select max(total_laid_off)
from layoffs_staging;

#saw a one hundred percent laid off for some companies (they went under), lets take a look
select *
from layoffs_staging
where percentage_laid_off = 1
order by total_laid_off desc; 

select company, sum(total_laid_off)
from layoffs_staging
group by company
order by 2 desc;

#look at time period, end of 2022 to beginning of march in 2023-- short time span
select min(`date`), max(`date`)
from layoffs_staging;

select industry, sum(total_laid_off)
from layoffs_staging
group by industry
order by 2 desc;

select country, sum(total_laid_off)
from layoffs_staging
group by country
order by 2 desc;

select year(`date`), sum(total_laid_off)
from layoffs_staging
group by year(`date`)
order by 1 desc;

select stage, sum(total_laid_off)
from layoffs_staging
group by stage
order by 2 desc;


#totals by month n year --this works here since you have less than a year worth of data
select substring(`date`, 6, 2) as `month`, sum(total_laid_off)
from layoffs_staging
group by `month`;

#to include the year, use this on
select substring(`date`, 1, 7) as `month`, sum(total_laid_off)
from layoffs_staging
group by `month`;

#rolling sum
with rolling_total as (
select substring(`date`, 1, 7) as `month`, sum(total_laid_off) as total_off
from layoffs_staging
group by `month`
)

select `month`, total_off, sum(total_off) over(order by `month`) as rolling_tot
from rolling_total;
#from this query, we see january of 2023 had a huge spike 


#this would find who laid off more people per year if there was more data
select company, sum(total_laid_off)
from layoffs_staging
group by company
order by 2 desc;

select company, year(`date`), sum(total_laid_off)
from layoffs_staging
group by company, year(`date`)
order by 3 desc;


with company_year as(
select company, year(`date`) as `year`, sum(total_laid_off) as sum
from layoffs_staging
group by company, year(`date`)
), 
company_year_rank as(
select *, dense_rank() over(partition by `year` order by sum desc) as ranking
from company_year
where `year` is not null)

select *
from company_year_rank
where ranking <=5;


select *
from layoffs_staging;