import { Component } from '@angular/core';
import { Validators, UntypedFormGroup, UntypedFormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

import { AuthService } from '../../../shared/services/auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {

  emailRegx = /^(([^<>+()\[\]\\.,;:\s@"-#$%&=]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
  public hide = true;
  public loginForm: UntypedFormGroup = this.formBuilder.group({
      email: [null, [Validators.required, Validators.pattern(this.emailRegx)]],
      password: [null, Validators.required]
  });

  public loading: boolean = false;

  constructor(
    private authService: AuthService,
    private _snackBar: MatSnackBar,
    private router: Router,
    private formBuilder: UntypedFormBuilder
  ) {}

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 2000,
    });
  }

  public submit(): void {
    if(!this.loginForm?.valid) {
      this._snackBar.open('Please provide vaild values.', 'Close');
    } else {
    const email = this.loginForm.value.email;
    const password = this.loginForm.value.password;
    this.loading = true;
    this.authService
      .login(email, password)
      .subscribe(() => {
        
        if (this.authService.isLoggedIn.getValue() == true) {
          if (this.authService.redirectUrl != "") {
            this.router.navigate([this.authService.redirectUrl]);
            this.authService.redirectUrl = "";
          }else {
            this.router.navigate(['/feed']);
          }
        }
        this.loading = false;
      }, error => {
          if (error.status >= 400 && error.status < 500) {
            this._snackBar.open('Error. Credentials are invalid!', 'Close');
            this.loading = false;
          }
      });
    }
  }
}