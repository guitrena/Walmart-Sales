# Walmart-Sales 

:warning: <span style="color:red"> Modelling in process</span>.

## 0. Introduction

This project is based on a **competition found in Kaggle launched by the Walmart's Recruiting team**. The link to the competition is: https://www.kaggle.com/competitions/walmart-recruiting-store-sales-forecasting/overview

The competition's description is as follows: "In this recruiting competition, job-seekers are provided with historical sales data for 45 Walmart stores located in different regions. Each store contains many departments, and participants must project the sales for each department in each store. To add to the challenge, selected holiday markdown events are included in the dataset."

The objective of the competition was to predict weekly sales for each store, department, and date. Participants were required to submit predictions for a year using historical data from previous years. _For the predictions, only the features were provided, without access to the target variable, making it impossible to evaluate performance on the test set._ 

Although not explicitly required, we will perform a thorough analysis. Due to the large volume of data and the variety of departments, we have defined a methodology for analyzing sales across departments, starting with the development of a dashboard. Following this, a few example cases will be presented.

## 1. Data


### Datasets Overview

The project is composed of **4 different datasets:**
- **stores.csv:** contains anonymized information about the 45 stores, indicating the type and size of store.
- **train.csv:** the historical training data, which covers to 2010-02-05 to 2012-11-01. 
> This file contains the following fields:
>
>Store - the store number <br>
>Dept - the department number <br>
>Date - the week  <br>
>Weekly_Sales -  sales for the given department in the given store <br>
>IsHoliday - whether the week is a special holiday week <br>
- **test.csv:** This file is identical to train.csv, except there is no weekly sale.
- **features.csv:** This file contains additional data related to the store, department, and regional activity for the given dates. 
>It contains the following fields:
>
>Store - the store number <br>
>Date - the week<br>
>Temperature - average temperature in the region<br>
>Fuel_Price - cost of fuel in the region<br>
>MarkDown1-5 - anonymized data related to promotional markdowns that Walmart is running. Any missing value is marked with an NA.<br>
>CPI - the consumer price index<br>
>Unemployment - the unemployment rate <br>
>IsHoliday - whether the week is a special holiday week

**In the *data.ipynb* notebook, these datasets were merged into one.** 


### Handling Missing Values

The only missing values are in the markdown features (MarkDown1 to 5). These features have no data before 11-11-2011, and even after that date, some values remain missing. Therefore, while the full dataset spans nearly three years, markdown data is only available for one year.   

<p align="center">
  <img src="./Images/period_markdown_data.png" />
</p>

Markdowns are store-specific, making it difficult to fill missing values. To address this, we examined the trends of these variables across store types, plotting the mean, maximum, and minimum values over time _(see the data_exploration.ipynb notebook)_. We found that stores of the same type displayed similar trends and dimensions. Based on this, we filled missing values using the average for the corresponding store type and date. When no data was available for any store in a given group, we used 0 as the default value.

However, we still have missing values for the initial period, where no markdown data is available. This issue will be addressed during the modeling phase.


## 2. Analysis

### data_exploration.ipynb file

In this notebook, we conduct data exploration to better understand the dataset. The analysis is divided into the following sections:

- **Removing Negative Sales** Filtering out rows where weekly sales are negative, as they are not valid.
- **Store types:** Understanding store classification and reclassifying two stores based on size and department presence.
- **Filling Missing Markdowns:** Explained in section _1. Data (Fill NA Values)_
- **By Department:** Grouping data by department to obtain general statistics (e.g., sales, percentage of total sales). Additionally, performing ANOVA tests to examine correlations between qualitative variables ('IsHoliday') and 'Weekly_Sales', with boxplots created if significant (p-value < 0.01). Finally, performing Pearson correlation tests are used for quantitative variables ('Temperature', 'CPI', 'Unemployment', 'Fuel_Price'), and regression plots are displayed if the correlation is significant (p-value < 0.01).
- **Example Cases:** Visualizing necessary graphs to analyze specific cases.

### Dashboard

As mentioned earlier, the dataset is large and needs to be segmented for focused analysis. A dashboard was developed to facilitate this, providing various analysis elements for individual departments. While not definitive for drawing conclusions, it helps to understand department behavior and serves as a starting point for hypothesis generation.

<p align="center">
  <img src="./Images/dashboard_example28.png" />
</p>

>The dashboard consists of four sections:
> - **Department Selection:** Allows users to select a department through a dropdown menu and display its information using a button.
> - **General stats:**
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- General: Time period, total sales, percentage of overall sales, and sales ranking.<br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- Store Presence: Percentage of stores carrying the department, broken down by store type.<br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- Distribution of Weekly Sales: A boxplot of weekly sales for the selected department over the specified period.
> - **Seasonal Decompose:** Displays the observed sales, trend, seasonal, and residual components for the selected department's weekly sales.
> - **Weekly Sales correlation with other features:** : Regression plots for quantitative variables if a significant Pearson test result (p-value < 0.01) is found, and boxplots for qualitative variables if ANOVA results are significant. If no significant correlation is found, the plot is grayed out with a message displaying the p-value. Five tests are performed:
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- Temperature vs Weekly_Sales <br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- IsHoliday vs Weekly_Sales <br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- CPI vs Weekly_Sales <br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- Unemployment vs Weekly_Sales <br>
>> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- Fuel_Price vs Weekly_Sales 

### Example Cases

To demonstrate the dashboard's utility, we explore two example departments. The dashboard serves as a starting point for examining various factors influencing sales dynamics in the department.

It is important to note that the dataset is anonymized, making it more difficult to analyze since contextual details are missing.

#### Department 28

<p align="center">
  <img src="./Images/dashboard_example28.png" />
</p>

In the dashboard, we see that sales in this department are correlated with temperature, CPI, unemployment, and fuel prices. However, this correlation does not necessarily imply causality. 

> To further investigate the relationship between temperature and sales, we plotted the two variables over time.
>
><p align="center">
>  <img src="./Images/temperature_sales28.png" />
></p>
>
> Based on the graph, it seems reasonable to conclude that lower temperatures may drive higher sales in this department. However, further context is needed to confirm this hypothesis.

> For the other correlated features, the regression plots are less clear compared to the temperature plot. To dig deeper, we plotted the evolution of these features over time.
><p align="center">
>  <img src="./Images/economic_indicators.png" />
></p>
> The trends for CPI, fuel prices, and unemployment are evident: CPI and fuel prices are rising, while unemployment is decreasing. Department 28’s sales also exhibit a decreasing trend, dropping by around 14%. This explains the correlation between sales and these features. <br>
><br><p align="center">
>  <img src="./Images/trend28.png" />
></p>
>  However, we cannot definitively conclude causality because of the lack of contextual information. For instance, the second winter period had warmer temperatures, which could explain the decrease in sales.

##### _Conclusions_

- **Sales in this department are influenced by temperature.** Lower temperatures are associated with higher sales.
- **Sales trend decreasing by 14%.** This decline could be attributed to rising CPI or warmer winters, but further context is required to confirm either hypothesis.

#### Department 22


<p align="center">
  <img src="./Images/dashboard_example22.png" />
</p>

The dashboard indicates correlations between sales in this department and all the key variables. However, correlation does not necessarily imply causality.

> To further investigate the relationship between temperature and sales, we plotted both variables over time.
>
><p align="center">
>  <img src="./Images/temperature_sales22.png" />
></p>
>
> The graph suggests that temperature does not significantly affect sales, which remain stable except for two peaks. We will explore these peaks below.

> To investigate the relationship between holidays periods and sales we plotted them.
>
><p align="center">
>  <img src="./Images/holidays_sales22.png" />
></p>
>
> The two peaks align precisely with Thanksgiving and Christmas. As shown in the dashboard’s seasonal plot, sales during these weeks are almost 100% higher than usual.

> For the remaining features (CPI, Unemployment, Fuel Price), the relationship is similar to Department 28. CPI and fuel prices trend upward, unemployment trends downward, and sales in Department 22 show a decreasing trend (8.7%).
>
><p align="center">
>  <img src="./Images/trend22.png" />
></p>
>
> However, without additional context, we cannot assert causality.

##### _Conclusions_
- **Two sales peaks occur during Thanksgiving and Christmas (+100%).**
- **Sales trend decreasing by 8.7%.** This may be linked to rising CPI, though further context is needed..

## 3. Modelling

The original competition aimed to estimate the weekly sales for the test set, but in our case, we are estimating the sales for the last year of data to compare the predictions with the actual values. Therefore, the markdown features (which are only present for the last year) were removed since we cannot extrapolate these for the entire year without further information about these variables.

### Process 

When it comes to modeling, the first critical step is choosing the right strategy. This becomes even more important when dealing with a large dataset that needs to be broken down into manageable parts.

In this case, we trained several models by considering each combination of department and store. The selected models were similar in nature:
- **SARIMA:** A time series forecasting model designed to handle data with seasonal patterns.
- **SARIMAX:** An extension of SARIMA that includes external variables to enhance the analysis.

After selecting the models, we implemented a strategy to choose the external variables for each model. This was based on the results of the ANOVA and Pearson tests conducted earlier, which compared each feature to the Weekly Sales. If a feature showed significant correlation, it was included in the SARIMAX model. For some cases where no features were correlated, the SARIMAX model was not trained.

To save time, the models were trained using **AUTO ARIMA**, which automatically selects the appropriate terms for each model.

Finally, we plotted the historical data alongside the forecast to analyze the results.

Additionally, we decided to limit this strategy to a reduced number of models. Specifically, we chose to train models only for **Departments 22 and 28, and Store 1**, which reduced the number of cases from 3,211 to 160. This decision was due to computational constraints. For example, the batch selected took nearly 6 hours to process. By estimating the time required to train the entire dataset, it would have taken approximately 120 hours.

Below is a diagram summarizing the entire process:
<p align="center">
  <img src="./Images/process_diagram.png" />
</p>

### Results

We trained the Store-Department combinations for the following:
- Department 22
- Department 28
- Store 1

For each group, we present a summary that shows the best, average, and worst error percentage (RMSE/Average Weekly Sales) within the group. We also show the percentage breakdown of the best-performing models, categorized as **SARIMA** (no SARIMAX trained), **SARIMA(x)** (SARIMA was the best model between the two), and **SARIMAX** (SARIMAX was the best model between the two).

After that, we plot and analyze the best and worst cases within each group, correcting the model if necessary.

#### Department 22

> **Summary key points:**
> - Minimum and average percentage errors are relatively similar. The difference seems to stem from extreme values (the worst case having a 47.62% error).
> - More than 70% of combinations have correlated features.
> - External variables are relevant in only 32% of the cases.
>
><p align="center">
>  <img src="./Images/summary22.png" />
></p>

> **Best prediction:** Store 23 with a 12.13% error. Key points:
> - The model used is **SARIMA.**
> - The worst predictions are during two sales peaks (Christmas and the last week of August).
> - The Christmas peak is not as poorly predicted as it seems. The week before Christmas is overestimated by 5,954, and Christmas week is underestimated by 6,784. If these two weeks are aggregated into a "Christmas period," the underestimation is just 838 for the whole period.
> - As for the second period (August), we lack context to explain the peak. Without knowing what the department represents and where the store is located, it is difficult to understand the underestimation fully.
>
><p align="center">
>  <img src="./Images/best22.png" />
></p>

> **Worst prediction:** Store 39 with a 47.62% error. Key points:
> - The model used is **SARIMA.**
> - It is clear that the terms selected for the ARIMA model are incorrect.
> - After correcting the model, by adjusting the AUTO ARIMA range (specifically, modifying the "D" value, which was preset to 1), the error was reduced from 47.62% to 15.06%. This correction also brought down the average error from 20.21% to 19.33%.
> - Other cases may have similar issues.
><p align="center">
>  <img src="./Images/worst22.png" />
></p>
>
> After the correction, the model changed from ARIMA(1,0,1)(1,1,0)[52] to ARIMA(1,1,2)(1,0,0)[52].
>
><p align="center">
>  <img src="./Images/worst22_corrected.png" />
></p>

#### Department 28
> **Summary key points:**
> - The worst case shows an extremely high error percentage (119.76%).
> - 95% of combinations show correlated features, but only 23% of cases performed better with the SARIMAX model.
>
><p align="center">
>  <img src="./Images/summary28.png" />
></p>

>**Best prediction:** Store 23 with a 12.13% error. Key points:
> - The best model is **SARIMA** (SARIMAX also trained).
> - SARIMA generally tends to overestimate sales, while SARIMAX usually underestimates, a combination of both may be better.
><p align="center">
>  <img src="./Images/best28.png" />
></p>

> The worst prediction is for store 39 with 119.76% of error. Key points:
> - The model used is **SARIMA.**
> - The high error percentage is driven by an extreme peak in sales during the last week of May. This peak occurred in 2011 but was not present in 2010 or 2009. We lack contextual information about the department and location to explain the sudden spike in 2011.
>
><p align="center">
>  <img src="./Images/worst28.png" />
></p>

#### Store 1

> **Summary key points:**
> - The worst case has a significant error percentage (175.1%).
> - The best case, however, shows a very strong result with an error of only 4.12%.
> - 70% of combinations show correlated features, but only 29% of the cases perform better with the SARIMAX model.
><p align="center">
>  <img src="./Images/summary1.png" />
></p>

>**Best prediction:** Department 95 with a 4.12% error. Key points:
> - The best model is **SARIMAX** (SARIMA also trained).
> - The prediction is quite accurate.
><p align="center">
>  <img src="./Images/best1.png" />
></p>

>**Worst prediction:** Department 59 with a 175.1% error. Key points:
> - The best model is **SARIMA** (SARIMAX also trained).
> - The high error is primarily due to an overestimation during the Christmas sales peak. In 2011, the peak was three times larger than in 2012, leading to the significant overestimation.
> - Without more context, it's difficult to explain the large variation between the two years.
> - Although SARIMA had a better RMSE, the SARIMAX model performed better when excluding the peak.
><p align="center">
>  <img src="./Images/worst1.png" />
></p>

## 4. Next steps
- Train additional models (e.g., regression models) and apply bagging techniques.
- Develop dashboards to analyze store or Store-Department combinations.
- Train and optimize models for all Store-Department combinations.

