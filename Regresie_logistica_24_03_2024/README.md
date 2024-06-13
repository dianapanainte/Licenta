# Logistic Regression

* first try to implement logistic regression using the LogisticRegression implemented in sklearn
* some features were one hot encoded and then scaled
* the dataset is split into train and test, but in chronological order, so as to not introduce data leakage
* features used: 'Difference_in_ranks', 'Different_hand', 'Age', 'Rank', 'Height', 'Wins_semester', 'Losses_semester',
                    "Wins_year", "Losses_year", "Wins_career", "Losses_career", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
                    "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
                    "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_career", "Opponent_Losses_career", "Opponent_Wins_clay",
                    "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
                    "Opponent_Losses_grass", "Hand_L", 'Hand_R', "Opponent_Hand_L", 'Opponent_Hand_R'
* (it is possible that some of the features are not useful, but I will try to use them all for now)
* and an important part is the fact that a match is represented by two rows, one for each player, with the target being the result of the match, with the small problem of the fact that i don't know if this is okay
* the model is trained on the train set and tested on the test set
* the model has an accuracy of 0.62 on the test set from 2022-2023
* the model has an accuracy of 0.654 on the test set from 2011-2012 (maybe players were more consistent in the past?)
* the model is saved using joblib???? -> I will try to use this -> done

# About files

* features.py - first try of engineering features, those from above
* Features_2_0.py - pretty much the same features, maybe some are out, the important part is the chronological split, and the fact that there are more years. Also, split is done by years (maybe without 2020, weird year) -> also, there are better results in the previous years
* Features_3_0.py - same features, but there is only 1 row per game, output assigned randomly
     
* LogisticRegression_3_1.py - the model based on Features_3_0.py, but the actual model is implemented using PyTorch

# About plots in Regresie_logistica_24_03_2024/Plots

* confusion_matrix_2011_2012.png - confusion matrix for the test set from 2011-2012
* confusion_matrix_2022_2023.png - confusion matrix for the test set from 2022-2023
