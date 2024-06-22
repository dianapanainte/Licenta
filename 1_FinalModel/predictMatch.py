import keras
import joblib
import pandas as pd

lr_model = keras.models.load_model('F:/GithubCloning/Licenta/1_FinalModel/models/LR_model.pkl')
model1 = keras.models.load_model('F:/GithubCloning/Licenta/1_FinalModel/models/ann_validation.keras')
model2 = keras.models.load_model('F:/GithubCloning/Licenta/1_FinalModel/models/ann_tournament.keras')
meta_model = keras.models.load_model('F:/GithubCloning/Licenta/1_FinalModel/models/meta_model.keras')


# -----------------PREPARING THE DATA FOR THE FIRST NEURAL NETWORK-----------------
def prepare_data_for_model1(data):
    ann_encoder_hand = joblib.load('F:/GithubCloning/Licenta/1_FinalModel/encoders/ann_encoder_hand.joblib')
    ann_encoder_opponent_hand = joblib.load(
        'F:/GithubCloning/Licenta/1_FinalModel/encoders/ann_encoder_opponent_hand.joblib')

    data_encoded = ann_encoder_hand.fit_transform(data[['Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_encoder_hand.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    data = pd.concat([data, data_encoded_df], axis=1)

    data_encoded = ann_encoder_opponent_hand.fit_transform(data[['Opponent_Hand']])
    data_encoded_df = pd.DataFrame(data_encoded.toarray(),
                                   columns=ann_encoder_opponent_hand.get_feature_names_out(['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    data = pd.concat([data, data_encoded_df], axis=1)
    return data
