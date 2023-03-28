import { Component, Inject, OnInit } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { map, retry } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { Currency } from '../../models/currency.model'; 
import { AuthService } from '../../services/auth/auth.service';
import { environment } from 'src/environments/environment';

interface CurrencyGroup {
  name: string;
  currencies: Currency[];
}

interface PortfolioPart {
  id?: number;
  currency: Currency;
  amount: number;
}

@Component({
  selector: 'app-edit-portfolio',
  templateUrl: './edit-portfolio.component.html',
  styleUrls: ['./edit-portfolio.component.scss']
})
export class EditPortfolioComponent implements OnInit {

  constructor(private _snackBar: MatSnackBar, private authService: AuthService, private httpClient: HttpClient, @Inject(DOCUMENT) private _document: Document,) { }
  public portfolioForm = new UntypedFormGroup({
    currency: new UntypedFormControl('', Validators.required),
    amount: new UntypedFormControl('', [Validators.required, Validators.pattern('[0-9]+(\.[0-9]+)?'), Validators.min(0.000000000000000000001)]),
  });

  public portfolio: PortfolioPart[] = [];
  public currencyGroups: CurrencyGroup[] = [];

  public selectedValue: string = '';

  ngOnInit(): void {
    this.getCurrencies().subscribe((data) => {
      this.currencyGroups = this.splitCurrencies(data);
    });

    this.getPortfolioById().subscribe((data) => {
      this.portfolio = data;
      this.updateAvailableCurrencies();
    });
  }

  getCurrencyErrorMessage(): string {
    return (this.portfolioForm.controls.currency.hasError('required')) ? $localize`:This field is mandatory.@@mandatoryFieldID:This field is mandatory.` : ''
  }
  
  getAmountErrorMessage(): string {
    if (this.portfolioForm.controls.amount.hasError('pattern')) {
      return $localize`:Provide valid number.@@invalidNumberErrorID:Provide a valid number. Use dot as a separator.`;
    } else if (this.portfolioForm.controls.amount.hasError('required')) {
      return $localize`:This field is mandatory.@@mandatoryFieldID:This field is mandatory.`;
    } else {
      return '';
    }
  }

  splitCurrencies(currencies: Currency[]): CurrencyGroup[] {
    let groups: CurrencyGroup[] = [
      {'name': 'fiat', 'currencies': []},
      {'name': 'crypto', 'currencies': []}
    ];
    for (let currency of currencies) {
      if (currency.currency_type == 'fiat') {
        groups[0].currencies.push(currency);
      } else {
        groups[1].currencies.push(currency);
      }
    }
    return groups;
  }

  getPortfolioById(): Observable<PortfolioPart[]> {
    const PORTFOLIO_ENDPOINT = 'portfolios';
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + PORTFOLIO_ENDPOINT + '/', options=options).pipe(
      retry(2),
      map((data: any) => {
        return data.components;
      })
    );
  }

  savePortfolio(): void {
    let portfolio: Object[] = [];
    for (let part of this.portfolio) {
      portfolio.push(
        {
          'currency_id': part.currency.id,
          'amount': part.amount
        }
      )
    }
    this.postPortfolio(portfolio).subscribe(() => {
      this._document.defaultView?.location.reload();
    });
  }

  postPortfolio(portfolio: Object[]): Observable<any> {
    const PORTFOLIO_ENDPOINT = 'portfolios';
    let options = this.authService.getOptions();
    return this.httpClient.post(environment.apiEndpoint + PORTFOLIO_ENDPOINT + '/', portfolio, options=options);
  }

  getCurrencies(): Observable<Currency[]> {
    const CURRENCY_ENDPOINT = 'currencies';
    let options = this.authService.getOptions();
    return this.httpClient.get(environment.apiEndpoint + CURRENCY_ENDPOINT + '/', options=options).pipe(
      retry(2),
      map((data: any) => {
        return this.parseToCurrency(data.data);
      })
    );
  }

  parseToCurrency(data: any): Currency[] {
    return data
  }

  addPart(): void {
    if (this.portfolioForm.valid) {
      try {
        const part: PortfolioPart = {
          'amount': parseFloat(this.portfolioForm.value.amount),
          'currency': this.portfolioForm.value.currency
        }
        this.portfolio.push(part);
        this.portfolioForm.reset();
      } catch (error) {
        
      }

    }
    this.updateAvailableCurrencies();
  }

  deletePart(part: PortfolioPart): void {
    const index: number = this.portfolio.indexOf(part);
    if (index > -1) {
      this.portfolio.splice(index, 1);
    }
    this.updateAvailableCurrencies();
  }

  updateAvailableCurrencies(): void {
    let selectedCurrencies: string[] = [];
    for (let part of this.portfolio) {
      selectedCurrencies.push(part.currency.acronym);
    }

    for (let groupIndex = 0; groupIndex < this.currencyGroups.length; groupIndex++) { // iterate over each group
      for (let currencyIndex = 0; currencyIndex < this.currencyGroups[groupIndex].currencies.length; currencyIndex++) { // iterate over each currency
        let disabled: boolean = false;
        if (selectedCurrencies.indexOf(this.currencyGroups[groupIndex].currencies[currencyIndex].acronym) > -1) {
          disabled = true;
        }
        this.currencyGroups[groupIndex].currencies[currencyIndex].disabled = disabled;
      }
    }
  }
}
