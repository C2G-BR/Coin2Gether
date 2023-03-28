import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, retry } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Trade } from '../../models/trade.model';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class TradeService {

  constructor(private httpClient: HttpClient, private authService: AuthService) { }

  TRADES_ENDPOINT = 'trades';
  
  public getCurrencies(): Observable<any> {
    return this.httpClient.get(environment.apiEndpoint + '/getCurrencies').pipe(
      retry(2),
      map((data: any) => {
        return data.data
      })
    );
  }

  public getAllTrades(): Observable<Trade[]> {
    return this.httpClient.get(environment.apiEndpoint + this.TRADES_ENDPOINT + '/').pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((trade: Trade) => {
          return this.isTrade(this.parseToTrade(trade));
        });
      })
    );
  }

  public getAllFollowedTrades(): Observable<Trade[]> {
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + this.TRADES_ENDPOINT + '/followed', options=options).pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((trade: Trade) => {
          return this.isTrade(this.parseToTrade(trade));
        });
      })
    );
  }

  public getTradesByAuthor(author: String): Observable<Trade[]> {
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + this.TRADES_ENDPOINT + '/' + author, options=options).pipe(
      retry(2),
      map((data: any) => {
        return data.data.filter((trade: Trade) => {
          return this.isTrade(this.parseToTrade(trade));
        })
      })
    );
  }

  public getTradeById(id: number): Observable<Trade> {
    return this.httpClient.get(environment.apiEndpoint + this.TRADES_ENDPOINT + '/' + id.toString()).pipe(
      retry(2),
      map((data: any) => {
        return this.parseToTrade(data);
      })
    );
  }

  private parseToDate(dateString: any): Date {
    let date = new Date(dateString);
    date = date ? date : new Date();
    return date;
  }

  private parseToTrade(data: any): Trade {
    data.interface = "trade";
    data.date = this.parseToDate(data.date);
    data.startdate = this.parseToDate(data.startdate);
    data.enddate = this.parseToDate(data.enddate);
    try {
      data.fiatcurrency = data.debit_currency.acronym;
      data.cryptocurrency = data.credit_currency.acronym;
    } finally {
      return data;
    }
  }

  private isTrade(trade: Trade): Boolean {
    try {
      if (!isNaN(this.parseToDate(trade.date).getTime()) && !isNaN(trade.startdate.getTime()) && !isNaN(trade.enddate.getTime())) {
        return true
      } else {
        return false;
      }
    } catch (error) {
      return false
    }
  }
}
