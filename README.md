# the_iconic

This project infers gender from sales data.

# Summary

The dataset is unlabelled, hence K-means clustering was used to try to cluster the users into genders ("male", "female"). Four different models were fitted, each having a different number of clusters; 2, 3, 4, 5. Models with more than 2 clusters were considered in light of the non-binary genders such as androgyne, transgender etc.

None of the models were performant, i.e. from an analysis of the distributions, none of the different clusters were able to separate users who mostly purchased male items from users who most purchased female items, i.e. the most salient metrics in this exercise, see [Modelling Approach](#Modelling-Approach) below for further discussion.

The next steps include gather more granular data as well as variety of data such as brands purchased, item size etc; see [Next steps](#Next-steps).

The remainder of this document contains high-level summaries on the different aspects of EDA and modelling, please see the notebook `./notebooks/analysis.ipynb` for more details.

# Data evaluation and cleaning

For a Pandas Profile report of the raw data, see `./reports/the_iconic_profile_report.html`.

The following lists the discrepancies and any corrections made:

1. `days_since_last_order` is not in the correct scale (seemed to be in hours). It was divided by 24.
1. There are 249 duplicates rows, which was dropped.
1. The following columns don't add up to `items`, nor did they the gendered constituents add up to the `male_items` nor `female_items`. Difference combinations were also tried, to no avail. Hence they were dropped.
   1. `wapp_items`
   1. `mapp_items`
   1. `wftw_items`
   1. `mftw_items`
   1. `wacc_items`
   1. `macc_items`
   1. `wspt_items`
   1. `mspt_items`
   1. `curvy_items`
   1. `sacc_items`
1. Six rows were found to have more `cancels` than `orders`, which were dropped.
1. The following columns were binary, contrary to their descriptions; no actions were taken:
   1. `cc_payments`
   1. `paypal_payments`
   1. `afterpay_payments`
   1. `apple_payments`
1. Many values had a 0 `vouchers` but positive `average_discount_used`, so the `vouchers` feature was dropped.
1. `average_discount_used` seemed to be in a different scale, this was divided by 10,000.
1. Some rows had `revenue` smaller than the `average_discount_onoffer`, so the `average_discount_onoffer` feature was dropped.
1. Some rows had 0 `revenue`, 0 `cancels` and 0 `returns`, these were dropped.
1. `macc_items` and `wacc_items` are exactly the same. These were dropped in point 3 anyway.

The list of columns and `customer_id`s dropped are recorded in `./reports/artifacts/` directory, `cols_to_drop.csv` and `rows_to_drop.csv`, respectively.

While certain actions were taken, these should be confirmed by data engineering, and preferably fixed upstream rather than dropped.

## Feature engineeing

The features created are mostly related to percentages of constituents, due to the limited nature of the raw data.

1. `perc_male_items`
1. `perc_female_items`
1. `perc_unisex_items`
1. `items_per_order`
1. `days_between_first_and_last_order`
1. `rev_per_item`
1. `rev_per_order`
1. `perc_cancels`
1. `perc_returns`

Note that due to time restrictions, more features were not explored.

# Modelling approach

The goal of the clustering exercise is to be able to clearly assign users to a cluster with particular sets of traits. Typically, these sets of traits are discovered after the clustering exercise; through investigating the differences in the distributions of each feature between the clusters. After which a logical real-world label is applied to each cluster, e.g. "middle-aged men in NSW" are sufficiently different in their behaviour compared to other clusters.

However, in this case, there is already a prescribed label to achieve, i.e. "male" and "female", the traits of which should not be naively inferred from the clustering results because there is already a strongly established prior on male and female, i.e. it is well established that most males wear male clothes and most females wear female clothes. Furthermore, to the extent that the goal of the recommendations is to increase the probability of purchase of the item recommended, it can be argued that the inferred gender should merely be dependent on which gendered item the user has purchased the most of, i.e. recommend male items to users whose purchases have been more than X% male items.

With this goal in mind, the clustering should at least be able to separate the users into a cluster who purchased mostly male items and another cluster who purchased mostly female items.

## Model results

It turned out that none of the models were able to separate the user on this basis. The following chart shows two histograms of percentage of male vs female items purchases, based on the whole cleaned dataset. The peaks at 0 and 1 confirm our prior belief that most people either purchase only male items or purchase only female items, only very few purchase both.

![total_data](/reports/figures/image.png)

An ideal clustering result would have each panel showing only one peak, either near 0 or near 1, which would indicate that the people in that cluster has purchased either most male or mostly female. However, in all of the models (of different cluster size), the distribution shape shows the two peaks. For example, the following chart is from the model with two clusters (for more charts, see the notebook).

![two_clusters](/reports/figures/image-2.png)

It is possible to conduct statistical tests to check if these distributions are statistically significantly different to the one with the whole dataset, but I suspect that the effort would be better spend gather more data.

Another finding was that the 2-cluster model that included the additional features (see [Feature engineeing](#Feature-engineeing)) performed worse than the 2-cluster model with just the cleaned original features. This indicates that there would be some value in performing feature selection and more feature engineering.

## Conclusion

This modelling exercise was not able to satisfactorily achieve the goal of providing more effective recommendations.

# Next steps

The most impactful next steps would be gathering more data. The following are useful data in helping to define characteristics of the users.

1. Name - names are almost perfectly correlated with gender, though this is admittedly difficult to obtain for "guest" users.
1. Size data - people very slow change their body size, so they would typically purchase items of the same size.
1. Brands - some people are loyal to a small set of brands
1. Brand categories - such as luxury brand, surfing, casual
1. Colours - there is a strong gender preference of colour pallette, at least in the Western world.
1. Event level data - such as scrolling/clicking behaviour, this allows for richer feature engineering, allowing for more complex profiles per `customer_id`.

Discuss the discrepancies with the data engineering team, this could inform the appropriate actions to take in subsequent modelling exercises.

# Reproducibility

Follow these steps to run the notebook yourself. Make sure you have Python installed.

1. Clone this repo
1. Open a terminal
1. Change directory to the location of this repo locally
1. Create a `.env` file with the content:
   ```
   PASSWORD_HINT=<fill_this_in>
   ```
1. Install the dependencies:
   1. For `virtualenv`:
      1. `virtualenv venv`
      1. `venv\Scripts\activate`
      1. `pip install -f requirements.txt`
   1. For Conda environments:
      1. `conda env create -f environment.yml`
      1. `conda activate the_iconic`
1. You should have the following files:
   1. `.\the_iconic\data\raw\test_data.db.zip`
   1. `.\the_iconic\data\raw\test_data.zip`

# Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   └── raw            <- The original, immutable data dump.
    │
    ├── environment.yml    <- The dependencies for a Conda environment, generated with
    │                      <- `conda env export > environment.yml`
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── artifacts      <- Generated lists of columns, rows, to drop, and model results
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   ├── cleaner.py
        │   ├── make_dataset.py
        │   └── utils.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
