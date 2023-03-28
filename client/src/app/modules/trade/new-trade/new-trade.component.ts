import { Component, OnChanges, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Validators, UntypedFormGroup, UntypedFormBuilder, ValidatorFn, AbstractControl } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { UntypedFormControl } from '@angular/forms';
import { PublishTrade, Trade } from '../../../shared/models/trade.model';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../../shared/services/auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { TradeService } from 'src/app/shared/services/trade/trade.service';

function autocompleteStringValidator(validOptions: Array<string>): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } | null => {
    if (validOptions.indexOf(control.value) !== -1) {
      return null;
    }
    return { 'invalidAutocompleteString': { value: control.value } };
  }
}

interface Currencies {
  [key: string]: number;
}

@Component({
  selector: 'app-new-trade',
  templateUrl: './new-trade.component.html',
  styleUrls: ['./new-trade.component.scss']
})
export class NewTradeComponent implements OnInit {

  public fiatOptions: string[] = ['Euro €', 'US-Dollar $'];
  public cryptoOptions: string[] = ['Bitcoin', 'Bitcoin Cash'];
  public credit_curr: Currencies = {};
  public creditOptions:string[] = [];
  public debitOptions:string[] = [];
  public debit_curr: Currencies = {};

  public loaded1: boolean = false;
  public loaded2: boolean = false;

  minDate = new Date();
  maxDate = new Date();

  firstFormGroup: UntypedFormGroup = <UntypedFormGroup>{};
  secondFormGroup: UntypedFormGroup = <UntypedFormGroup>{};
  thirdFormGroup: UntypedFormGroup = <UntypedFormGroup>{};
  debitFilteredOptions: Observable<string[]> = <Observable<string[]>>{};
  creditFilteredOptions: Observable<string[]> = <Observable<string[]>>{};
  getCurrencies: Observable<any> = <Observable<any>>{};

  constructor(
    private formBuilder1: UntypedFormBuilder,
    private formBuilder2: UntypedFormBuilder,
    private formBuilder3: UntypedFormBuilder,
    private authService: AuthService,
    private tradeService: TradeService,
    private httpClient: HttpClient,
    private _snackBar: MatSnackBar,
    private router: Router,
  ) { }

  ngOnInit() {
    this.maxDate.setDate(this.minDate.getDate() + 5);
    let headers;
    try {
      const token = this.authService.getToken();
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': token
      });
    }catch {
      headers = new HttpHeaders({
        'Content-Type': 'application/json',
      });
    }

    let options = { headers: headers };
    this.httpClient.get(environment.apiEndpoint + 'currencies/user', options).subscribe((result: any) => {
      try {
        if(result.data.length == 0) {
          this.router.navigate(['/profile/' + this.authService.getUsername()]);
          this._snackBar.open('Error. Your current portfolio is empty. Please update your portfolio on your profile page!', 'Close');
        }else {
          for (let currency of result.data) {
            this.creditOptions.push(currency["name"]);
            this.credit_curr[currency["name"]] = currency["id"];
          }
        }
        this.loaded1 = true;
      } catch {
        this._snackBar.open('Error. There are some troubles with loading the currencies. Please try again!', 'Close');
      }
    }, error => {
      this._snackBar.open('Error. There are some troubles with reaching the server. Please contact our Admin!', 'Close');
    });

    this.httpClient.get(environment.apiEndpoint + 'currencies/', options).subscribe((result: any) => {
      try {
          for (let currency of result.data) {
            this.debitOptions.push(currency["name"]);
            this.debit_curr[currency["name"]] = currency["id"];
        }
        this.loaded2 = true;
      } catch {
        this._snackBar.open('Error. There are some troubles with loading the currencies. Please try again!', 'Close');
      }
    }, error => {
      this._snackBar.open('Error. There are some troubles with reaching the server. Please contact our Admin!', 'Close');
    });
    this.setFormGroups();
  }

  private setFormGroups() {
    this.firstFormGroup = this.formBuilder1.group({
      sellOrBuy: ['', Validators.required]
    });
    this.secondFormGroup = this.formBuilder2.group({
      debit: new UntypedFormControl('', [Validators.required, autocompleteStringValidator(this.debitOptions)]),
      credit: new UntypedFormControl('', [Validators.required, autocompleteStringValidator(this.creditOptions)]),
      percentReturn: ['', Validators.required],
      motivation: ['', Validators.required],
      percentInvest: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required],
      description: ['', Validators.required]
    });;
    this.thirdFormGroup = this.formBuilder3.group({
      acceptTerms: new UntypedFormControl('', [Validators.required])
    });;

    this.debitFilteredOptions = this.secondFormGroup.controls.debit.valueChanges
    .pipe(
      startWith(''),
      map(value => this.debitFilter(value))
    );

    this.creditFilteredOptions = this.secondFormGroup.controls.credit.valueChanges
    .pipe(
      startWith(''),
      map(value => this.creditFilter(value))
    );

  }

  public publishTrade() {
    const trade: PublishTrade = {
      start_date: this.secondFormGroup.value.startDate,
      end_date: this.secondFormGroup.value.endDate,
      motivation: this.secondFormGroup.value.motivation,
      description: this.secondFormGroup.value.description,
      expected_change: this.secondFormGroup.value.percentReturn,
      percentage_trade: this.secondFormGroup.value.percentInvest,
      debit_currency_id: this.debit_curr[this.secondFormGroup.value.debit],
      credit_currency_id: this.credit_curr[this.secondFormGroup.value.credit]
    }
    try {
      const token = this.authService.getToken();
      let headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': token
      });

      let options = { headers: headers };

      this.httpClient.post(environment.apiEndpoint + 'trades/', trade, options).subscribe(result => {
        this.router.navigate(['']);
      }, error => {
        this._snackBar.open('Error. There are some troubles with this trade. Please try again!', 'Close');
      });
    } catch (e) {
      this._snackBar.open('Error. No authorization token found. Please login again!', 'Close');
    }
  }

  formatLabelPercent(value: number) {
    return value + '%';
  }

  formatLabelTime(value: number) {
    return value + 'W';
  }

  private debitFilter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.debitOptions.filter(option => option.toLowerCase().includes(filterValue));
  }

  private creditFilter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.creditOptions.filter(option => option.toLowerCase().includes(filterValue));
  }
}