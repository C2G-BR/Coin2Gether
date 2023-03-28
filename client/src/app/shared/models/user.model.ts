import { Currency } from './currency.model';

export interface User {
    id?: number,
    username: string,
    email: string,
    firstName: string,
    lastName: string,
    street?: string,
    zip?: number,
    city?: string,
    country: string,
    password: string,
    birthdate: Date,
    join_date?: Date,
    follower?: number,
    following?: number,
    posts?: number,
    trades?: number,
    correct_trades?: number,
    wrong_trades?: number,
    links?: {
        name: string,
        link?: string,
        platform?: string
    }[],
    portfolio?: {
        components: {
            portfolio_name: string,
            amount: number,
            currency: Currency,
        }[],
    },
    follows?: Boolean,
    accounts?: {
        accounts: string,
        link?: string,
        socialMediaPlatform?: string
    }[]
    account?: {
        socialMediaAccount: string,
        socialMediaPlatform: string
    }
}

export interface UserUpdate {
    firstName: string,
    lastName: string,
    birthdate: Date,
    account?: {
        socialMediaAccount: string,
        socialMediaPlatform: string
    }
}