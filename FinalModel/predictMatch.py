import pickle
import keras
import joblib
import pandas as pd


# -----------------PREPARING THE DATA FOR THE FIRST NEURAL NETWORK-----------------
def prepare_data_for_model1(data):
    ann_encoder_hand = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/ann_encoder_hand.joblib')
    ann_encoder_opponent_hand = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_encoder_opponent_hand.joblib')

    all_possible_columns = ann_encoder_hand.get_feature_names_out(['Hand'])
    all_possible_columns = [col for col in all_possible_columns if col != 'Hand_U']
    data_encoded = ann_encoder_hand.fit_transform(data[['Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_encoder_hand.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_encoder_opponent_hand.get_feature_names_out(['Opponent_Hand'])
    all_possible_columns = [col for col in all_possible_columns if col != 'Opponent_Hand_U']
    data_encoded = ann_encoder_opponent_hand.fit_transform(data[['Opponent_Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_encoder_opponent_hand.get_feature_names_out(['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    # scale data for this model
    scaler = joblib.load('F:/GithubCloning/Licenta/FinalModel/scalers/ann_scaler.joblib')
    data = scaler.fit_transform(data)
    return data


def prepare_data_for_model2(data):
    # ann_tournament_encoder_player = joblib.load(
    #     'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_player.joblib')
    # ann_tournament_encoder_opponent = joblib.load(
    #     'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent.joblib')
    ann_tournament_encoder_hand = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_hand.joblib')
    ann_tournament_encoder_opponent_hand = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_opponent_hand.joblib')
    ann_tournament_encoder_tournament = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_tournament.joblib')
    ann_tournament_encoder_surface = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_surface.joblib')
    ann_tournament_encoder_round = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/ann_tournament_encoder_round.joblib')

    # all_possible_columns = ann_tournament_encoder_player.get_feature_names_out(['Player'])
    # data_encoded = ann_tournament_encoder_player.fit_transform(data[['Player']])
    # data_encoded_df = pd.DataFrame(data_encoded.toarray(),
    #                                columns=ann_tournament_encoder_player.get_feature_names_out(['Player']))
    # data.drop('Player', axis=1, inplace=True)
    # for col in all_possible_columns:
    #     if col not in data_encoded_df.columns:
    #         data_encoded_df[col] = 0
    # data = pd.concat([data, data_encoded_df], axis=1)
    #
    # all_possible_columns = ann_tournament_encoder_opponent.get_feature_names_out(['Opponent'])
    # data_encoded = ann_tournament_encoder_opponent.fit_transform(data[['Opponent']])
    # data_encoded_df = pd.DataFrame(data_encoded.toarray(),
    #                                columns=ann_tournament_encoder_opponent.get_feature_names_out(['Opponent']))
    # data.drop('Opponent', axis=1, inplace=True)
    # for col in all_possible_columns:
    #     if col not in data_encoded_df.columns:
    #         data_encoded_df[col] = 0
    # data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_tournament_encoder_hand.get_feature_names_out(['Hand'])
    all_possible_columns = [col for col in all_possible_columns if col != 'Hand_U']
    data_encoded = ann_tournament_encoder_hand.fit_transform(data[['Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_tournament_encoder_hand.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_tournament_encoder_opponent_hand.get_feature_names_out(['Opponent_Hand'])
    # all_possible_columns = [col for col in all_possible_columns if col != 'Opponent_Hand_U']
    data_encoded = ann_tournament_encoder_opponent_hand.fit_transform(data[['Opponent_Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_tournament_encoder_opponent_hand.get_feature_names_out(
                                       ['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_tournament_encoder_tournament.get_feature_names_out(['Tournament'])
    data_encoded = ann_tournament_encoder_tournament.fit_transform(data[['Tournament']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_tournament_encoder_tournament.get_feature_names_out(['Tournament']))
    data.drop('Tournament', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_tournament_encoder_surface.get_feature_names_out(['Surface'])
    data_encoded = ann_tournament_encoder_surface.fit_transform(data[['Surface']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_tournament_encoder_surface.get_feature_names_out(['Surface']))
    data.drop('Surface', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    all_possible_columns = ann_tournament_encoder_round.get_feature_names_out(['Round'])
    data_encoded = ann_tournament_encoder_round.fit_transform(data[['Round']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_tournament_encoder_round.get_feature_names_out(['Round']))
    data.drop('Round', axis=1, inplace=True)
    for col in all_possible_columns:
        if col not in data_encoded_df.columns:
            data_encoded_df[col] = 0
    data = pd.concat([data, data_encoded_df], axis=1)

    scaler = joblib.load('F:/GithubCloning/Licenta/FinalModel/scalers/ann_2_scaler.joblib')
    data = scaler.fit_transform(data)
    return data


def prepare_data_for_lr(data):
    lr_encoder_hand = joblib.load('F:/GithubCloning/Licenta/FinalModel/encoders/lr_encoder_hand.joblib')
    lr_encoder_opponent_hand = joblib.load(
        'F:/GithubCloning/Licenta/FinalModel/encoders/lr_encoder_opponent_hand.joblib')

    data_encoded = lr_encoder_hand.fit_transform(data[['Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=lr_encoder_hand.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    data = pd.concat([data, data_encoded_df], axis=1)

    data_encoded = lr_encoder_opponent_hand.fit_transform(data[['Opponent_Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=lr_encoder_opponent_hand.get_feature_names_out(['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    data = pd.concat([data, data_encoded_df], axis=1)

    scaler = joblib.load('F:/GithubCloning/Licenta/FinalModel/scalers/LR_scaler.joblib')
    data = scaler.transform(data)
    return data


def predict_match(data):
    print("Importing models")
    lr_file = 'F:/GithubCloning/Licenta/FinalModel/models/LR_model.joblib'
    lr_model = joblib.load(lr_file)
    model1 = keras.models.load_model('F:/GithubCloning/Licenta/FinalModel/models/ann_validation.h5')
    model2 = keras.models.load_model('F:/GithubCloning/Licenta/FinalModel/models/ann_tournament.h5')
    meta_model = keras.models.load_model('F:/GithubCloning/Licenta/FinalModel/models/meta_model.h5')

    data = pd.DataFrame(data)
    data_model_1 = data.drop(
        columns=['Player', 'Opponent', 'Tournament', 'Surface', 'Round', 'Difference_in_ranks',
                 'Different_hand'])
    data_model_2 = data.drop(columns=['Player', 'Opponent'])
    data_model_lr = data.drop(
        columns=['Player', 'Opponent', 'Tournament', 'Surface', 'Round', 'Hand', 'Opponent_Hand'])
    # preparing data
    data1 = prepare_data_for_model1(data_model_1)
    data2 = prepare_data_for_model2(data_model_2)
    print(data1.shape)
    print(f"Data2 : {data2.shape}")
    prediction1 = model1.predict(data1)
    prediction2 = model2.predict(data2)
    prediction_lr = lr_model.predict(data_model_lr)
    prediction1 = prediction1.ravel() if len(prediction1.shape) > 1 else prediction1
    prediction2 = prediction2.ravel() if len(prediction2.shape) > 1 else prediction2
    prediction_lr = prediction_lr.ravel() if len(prediction_lr.shape) > 1 else prediction_lr
    print(prediction1.shape)
    print(prediction2.shape)
    print(prediction_lr.shape)
    X_val_meta = pd.DataFrame(data={'Model1': prediction1, 'Model2': prediction2, 'LR': prediction_lr})
    meta_prediction = meta_model.predict(X_val_meta)
    return meta_prediction


def get_hi():
    return "Hello from Python!"
