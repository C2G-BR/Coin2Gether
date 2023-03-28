import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from app import db
from app.model.user import User, followers
from app.model.portfolio import Portfolio
from app.model.currency import Currency
from app.service.auth_service import get_user_from_token
from itertools import chain

from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

def build_portfolio_similarity_matrix():
    portfolios = Portfolio.query.all()
    currencies = Currency.query.all()
    currency_name = [currency.name for currency in currencies]
    df = pd.DataFrame()
    for portfolio in portfolios:
        components = {name: 0 for name in currency_name}
        num_components = len(portfolio.components)
        for component in portfolio.components:
            # Punish portfolios with many different currencies since these would generally be recommended more often.
            components[component.currency.name] = 1/num_components
        df = pd.concat([df, pd.DataFrame(components, index=[portfolio.user_id])])
    A_sparse_port = sparse.csr_matrix(df)
    similarities_port = cosine_similarity(A_sparse_port)
    sim_port = pd.DataFrame(similarities_port)
    sim_port.set_index(df.index, inplace = True)
    sim_port.columns = df.index
    return sim_port

def get_all_follows():
    entries = []
    with db.engine.connect() as connection:
        result = db.engine.execute(followers.select())
        for row in result:
            entries.append(row)
    entries = pd.DataFrame(entries, columns=['source', 'target'])
    return entries

def get_k_matching_user(ranks, user, k):
    follows = user.followers.with_entities(followers.c.follower_id).all()
    follows = list(chain.from_iterable(follows))
    # Do not recommend any user that is either the user itself or someone that the user already follows.
    follows.append(user.user_id)
    ranks = dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))
    list(map(ranks.__delitem__, filter(ranks.__contains__, follows)))

    ranks = list(ranks.keys())[:k]
    return ranks

def recommend_users(token):
    user = get_user_from_token(token)
    similarity_matrix = build_portfolio_similarity_matrix()
    follows = get_all_follows()
    G = nx.from_pandas_edgelist(follows, create_using = nx.DiGraph())
    personalization = similarity_matrix[user.user_id] if sum(similarity_matrix[user.user_id]) > 0 else None
    ranks = nx.pagerank(G, personalization=personalization)
    ranks = get_k_matching_user(ranks, user, 10)
    users = User.query.filter(User.user_id.in_(ranks)).all()
    return users