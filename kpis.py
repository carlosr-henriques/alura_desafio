import pandas as pd

def calculate_positive_feedbacks_kpi(df):

    total_feedbacks = len(df)
    feedbacks_positivos = len(df[df['sentiment'] == 'POSITIVO'])
    percentagem_positivos = (feedbacks_positivos / total_feedbacks) * 100
 
    return percentagem_positivos

def calculate_negative_feedbacks_kpi(df):

    total_feedbacks = len(df)
    feedbacks_negativos = len(df[df['sentiment'] == 'NEGATIVO'])
    percentagem_negativos = (feedbacks_negativos / total_feedbacks) * 100

    return percentagem_negativos

def calculate_inconclusive_kpi(df):

    total_feedbacks = len(df)
    feedbacks_inconclusivos = len(df[df['sentiment'] == 'INCONCLUSIVO'])
    percentagem_inconclusivos = (feedbacks_inconclusivos / total_feedbacks) * 100

    return percentagem_inconclusivos

def calculate_features_kpi(df):
    # Contar as features mais pedidas
    feature_counts = df['code'].value_counts().reset_index()
    feature_counts.columns = ['Feature', 'Count']

    return feature_counts