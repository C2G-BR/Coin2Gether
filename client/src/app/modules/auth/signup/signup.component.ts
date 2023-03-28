import { Component } from '@angular/core';
import { Validators, UntypedFormGroup, UntypedFormBuilder, UntypedFormArray, AbstractControl, FormControl, ValidatorFn } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

import { AuthService } from '../../../shared/services/auth/auth.service';
import { MustMatch } from '../../../shared/validators/must-match.validator';
import { UserService } from '../../../shared/services/user/user.service';
import { User } from '../../../shared/models/user.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {

  public hide1 = true;
  public hide2 = true;

  


  emailRegx = /^(([^<>+()\[\]\\.,;:\s@"-#$%&=]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
  passwordRegx = '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{8,}';

  minDate = new Date();
  maxDate = new Date();

  public loading: boolean = false;

  public socialMediaPlatforms: string[] = ["Facebook", "Instagram", "Twitter", "LinkedIn", "TikTok"];

  public signupForm: UntypedFormGroup = this.formBuilder.group({
    email: [null, [Validators.required, Validators.pattern(this.emailRegx)]],
    firstName: [null, Validators.required],
    lastName: [null, Validators.required],
    username: [null, Validators.required],
    birthdate: [null, Validators.required],
    country: [null, Validators.required],
    password: [null, [Validators.required, Validators.pattern(this.passwordRegx)]],
    confirmPassword: [null, Validators.required],
    acceptTerms: [null, Validators.required],
    accounts: this.formBuilder.array([])
  }, {
    validator: MustMatch('password', 'confirmPassword')
  });

  constructor(
    private authService: AuthService,
    private _snackBar: MatSnackBar,
    private router: Router,
    private formBuilder: UntypedFormBuilder,
    private userService: UserService,
  ) {
    this.maxDate.setFullYear(this.minDate.getFullYear() - 18);
    this.minDate.setFullYear(this.minDate.getFullYear() - 120);
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 2000,
    });
  }

  simpleAccounts() {
    return this.signupForm.get("accounts");
  }

  accounts(): UntypedFormArray {
    return this.signupForm.get("accounts") as UntypedFormArray
  }

  newAccount(): UntypedFormGroup {
    return this.formBuilder.group({
      socialMediaPlatform:  [null, Validators.required],
      username:  [null, Validators.required]
    })
  }

  addAccount() {
    this.getAccounts();
    this.accounts().push(this.newAccount());
  }

  getAccounts() {
    return this.signupForm.value.accounts;
  }

  removeAccount(indexAcc:number) {
    this.accounts().removeAt(indexAcc);
  }

  public submit() {
    const user: User = {
      username: this.signupForm.value.username,
      email: this.signupForm.value.email,
      firstName: this.signupForm.value.firstName,
      lastName: this.signupForm.value.lastName,
      country: this.signupForm.value.country,
      password: this.signupForm.value.password,
      birthdate: this.signupForm.value.birthdate,
      accounts: this.signupForm.value.accounts
    };
    this.loading = true;
    this.userService.createUser(user).subscribe(result => {
        this.authService.login(user.email, user.password).subscribe(() => {
        if (this.authService.redirectUrl != "") {
          this.router.navigate([this.authService.redirectUrl]);
          this.authService.redirectUrl = "";
        }else {
          
          this.router.navigate(['/profile/' + user.username]);
        }
        this.loading = false;
        });
    }, error => {
        this._snackBar.open('Error. There are some troubles with the signup!', 'Close');
        this.loading = false;
    });

  }

}