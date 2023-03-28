export interface Trade {
    interface?: "trade",
    id?: number,
    date?: Date,
    motivation: string,
    description: string,
    expectedIncrease: number,
    percent: number,
    startdate: Date,
    enddate: Date,
    fiatcurrency: string,
    cryptocurrency: string,
    author?: string
}

export interface PublishTrade {
    start_date: Date | string,
    end_date: Date | string,
    motivation: string,
    description: string,
    expected_change: number,
    percentage_trade: number,
    debit_currency_id: number,
    credit_currency_id: number 
}
