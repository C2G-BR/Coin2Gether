from app import db
from app.model import *
from app.service.user_service import *
import datetime
import random
from sqlalchemy import text
import pandas as pd

def get_matching_user(users: User, id:int):
    user = None
    for u in users:
        if u.user_id == id:
            user = u
            break
    return user

def get_matching_currency(currencies: User, name:str):
    currency = None
    for c in currencies:
        if c.name == name:
            currency = c
            break
    return currency
    

def saveAllToDB(data):
    db.session.add_all(data)
    db.session.commit()

def createPlatforms():
    twitter = SocialMediaPlatform(platform_name = "Twitter", platform_specific_link="https://www.twitter.com/")
    instagram = SocialMediaPlatform(platform_name = "Instagram", platform_specific_link="https://www.instagram.com/")
    facebook = SocialMediaPlatform(platform_name = "Facebook", platform_specific_link="https://www.facebook.com/")
    linkedin = SocialMediaPlatform(platform_name = "LinkedIn", platform_specific_link="https://www.linkedin.com/in/")
    tiktok = SocialMediaPlatform(platform_name = "TikTok", platform_specific_link="https://www.tiktok.com/@")
    db.session.add(twitter)
    db.session.add(instagram)
    db.session.add(facebook)
    db.session.add(linkedin)
    db.session.add(tiktok)
    db.session.commit()
    print('added: platforms')

def createCurrencies():
    currencies = []
    currencies.append(Currency(name='Bitcoin', acronym='BTC', currency_type='crypto', symbol="฿"))
    currencies.append(Currency(name='Ethereum', acronym='ETH', currency_type='crypto', symbol="Ξ"))
    currencies.append(Currency(name='Euro', acronym='EUR', currency_type='fiat', symbol='€'))
    currencies.append(Currency(name='US-Dollar', acronym='USD', currency_type='fiat', symbol="$"))
    currencies.append(Currency(name='Canadian-Dollar', acronym='CAD', currency_type='fiat', symbol="$"))
    currencies.append(Currency(name='Bitcoin Cash', acronym='BCH', currency_type='crypto', symbol=""))
    currencies.append(Currency(name='Dogecoin', acronym='DOGE', currency_type='crypto', symbol="Ɖ"))
    currencies.append(Currency(name='Litecoin', acronym='LTC', currency_type='crypto', symbol="Ł"))
    currencies.append(Currency(name='Yen', acronym='JPY', currency_type='fiat', symbol='¥'))
    currencies.append(Currency(name='Yuán', acronym='CNY', currency_type='fiat', symbol='¥'))
    saveAllToDB(currencies)
    print('added: currencies')

def createUsers():
    df = pd.read_csv('app/data/persons.csv')
    for idx, row in df.iterrows():
        register(username=row['username'], email=row['email'], lastName=row['lastName'], firstName=row['firstName'], password=row['password'], birthdate=row['birthdate'])
    register(username="ChefBesos", email="jeffbezos@gmail.com", lastName="Besos", firstName="Chef", password="Passwort123!", birthdate=str(datetime.datetime.today() - datetime.timedelta(days=20*365)))
    register(username="EronMisk", email="eronmisk@gmail.com", lastName="Misk", firstName="Eron", password="Passwort123!", birthdate=str(datetime.datetime.today() - datetime.timedelta(days=21*365)))
    register(username="billyShorts", email="billgates@gmail.com", lastName="Gates", firstName="Jill I'm Single", password="Passwort123!", birthdate=str(datetime.datetime.today() - datetime.timedelta(days=22*365)))
    register(username="Max", email="max@gmail.com", lastName="Mustermann", firstName="Max", password="Passwort123!", birthdate=str(datetime.datetime.today() - datetime.timedelta(days=23*365)))
    register(username="Herbert", email="herbert@gmail.com", lastName="Herbert", firstName="Herbert", password="Passwort123!", birthdate=str(datetime.datetime.today() - datetime.timedelta(days=90*365)))
    print('added: users')

def createSocialMediaAccounts():
    platform = SocialMediaPlatform.query.first()
    user = User.query.first()
    accounts = []
    accounts.append(SocialMediaAccount(platform=platform, user=user, username='elonmusk'))
    saveAllToDB(accounts)
    print('added: accounts')    

def createFollowers():
    users = User.query.all()
    df = pd.read_csv('app/data/follower.csv')
    for idx, row in df.iterrows():
        users[row['source']].followed.append(users[row['target']])
    db.session.commit()
    print('added: followers')  

def createPortfolios():
    users = User.query.all()
    for user in users:
        user.portfolio = Portfolio()
    saveAllToDB(users)
    print('added: portfolios')

def createComponents():
    currencies = Currency.query.all()
    portfolios = Portfolio.query.all()
    df = pd.read_csv('app/data/persons.csv')
    for idx, row in df.iterrows():
        components = []
        for currency in currencies:
            components.append(Component(portfolio=portfolios[idx], currency=currency, amount=row[currency.name]))
        saveAllToDB(components)
    print('added: components')

def createPosts():
    users = User.query.all()
    df = pd.read_csv('app/data/posts.csv')
    df[['date']] = df[['date']].apply(pd.to_datetime, errors='coerce')
    posts = []
    for idx, row in df.iterrows():
        user = get_matching_user(users, row['user'])
        if user is not None:
            posts.append(Post(title=row['title'], description=row['description'], user=user, date=row['date']))
    saveAllToDB(posts)
    print('added: posts')

def createTrades():
    users = User.query.all()
    currencies = Currency.query.all()
    df = pd.read_csv('app/data/trades.csv')
    datetime_cols = ['publish_date', 'start_date', 'end_date']
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, errors='coerce')
    trades = []
    for idx, row in df.iterrows():
        user = get_matching_user(users, row['author'])
        debit_currency = get_matching_currency(currencies=currencies, name=row['debit_currency'])
        credit_currency = get_matching_currency(currencies=currencies, name=row['credit_currency'])
        if not None in [user, debit_currency, credit_currency]:
            trades.append(
                Trade(
                    publish_date=row['publish_date'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    motivation=row['motivation'],
                    description=row['description'],
                    expected_change=row['expected_change'],
                    percentage_trade=row['percentage_trade'],
                    author=user,
                    debit_currency=debit_currency,
                    debit_amount=row['debit_amount'],
                    credit_currency=credit_currency,
                    credit_amount=row['credit_amount'],
                )
            )
        else:
            print(idx, row)
    saveAllToDB(trades)
    print('added: trades')

def create_view():
    try:
        last_posts = text("CREATE VIEW last_10_posts AS SELECT * FROM posts LIMIT 10;")
        db.engine.execute(last_posts)
        last_trades = text("CREATE VIEW last_10_trades AS SELECT * FROM trades LIMIT 10;")
        db.engine.execute(last_trades)
    except Exception as e:
        print(e)

    print('added: view')

def create_procedure():
    new_follow = text("CREATE PROCEDURE new_follow(src_user integer, tgt_user integer) LANGUAGE SQL AS $$ INSERT INTO followers VALUES (src_user, tgt_user); $$;")
    delete_follow = text("CREATE PROCEDURE delete_follow(src_user integer, tgt_user integer) LANGUAGE SQL AS $$ DELETE FROM followers WHERE follower_id = src_user AND followed_id = tgt_user; $$;")
    db.engine.execute(new_follow)
    db.engine.execute(delete_follow)
    print('added: procedure')

def create_procedure_and_trigger():
    sequence = text("""CREATE SEQUENCE table_follow_log_id_seq;""")
    table_follow_log = text("""CREATE TABLE follow_log ( log_id INTEGER NOT NULL DEFAULT nextval('table_follow_log_id_seq'), follower_id INTEGER NOT NULL, followed_id INTEGER NOT NULL, date timestamp without time zone NOT NULL, action_type varchar NOT NULL, PRIMARY KEY (log_id), FOREIGN KEY (followed_id) REFERENCES public.users (user_id) MATCH SIMPLE, FOREIGN KEY (follower_id) REFERENCES public.users (user_id) MATCH SIMPLE );""")
    procedure_new_follow = text("""CREATE OR REPLACE FUNCTION trigger_new_follow() RETURNS trigger AS $$ BEGIN INSERT INTO follow_log (follower_id, followed_id, date, action_type) VALUES (NEW.follower_id, NEW.followed_id, now(), 'Add'); RETURN NEW; END; $$ LANGUAGE 'plpgsql';""")
    procedure_delete_follow = text("""CREATE OR REPLACE FUNCTION trigger_delete_follow() RETURNS trigger AS $$ BEGIN INSERT INTO follow_log (follower_id, followed_id, date, action_type) VALUES (OLD.follower_id, OLD.followed_id, now(), 'Delete'); RETURN NEW; END; $$ LANGUAGE 'plpgsql';""")
    trigger_new_follow = text("""CREATE TRIGGER insert_follow_trigger AFTER INSERT ON followers FOR EACH ROW EXECUTE PROCEDURE trigger_new_follow();""")
    trigger_delete_follow = text("""CREATE TRIGGER delete_follow_trigger AFTER DELETE ON followers FOR EACH ROW EXECUTE PROCEDURE trigger_delete_follow();""")
    db.engine.execute(sequence)
    db.engine.execute(table_follow_log)
    db.engine.execute(procedure_new_follow)
    db.engine.execute(procedure_delete_follow)
    db.engine.execute(trigger_new_follow)
    db.engine.execute(trigger_delete_follow)
    print('added: procedure & trigger')

    
def generate():
    create_procedure()
    create_procedure_and_trigger()
    createPlatforms()
    createCurrencies()
    createUsers()
    createSocialMediaAccounts()
    createPortfolios()
    createComponents()
    createTrades()
    createFollowers()
    createPosts()
    create_view()